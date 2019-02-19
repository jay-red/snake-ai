from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from snake import SnakeGame
import random
import numpy as np
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import median, mean
from collections import Counter

game = SnakeGame( True )

def randomGames():
	for _ in range(5):
		game.reset( True )
		for _ in range(200):
			win = game.getWindow()
			win.getch()
			action = game.sample()
			#print action
			state, reward, alive = game.step( action )
			if not alive:
				break
        game.close()

#randomGames()
game.close()
print game.getState()

initial_games = 50000
goal_steps = 500
score_requirement = 900
LR = 1e-4

def initial_population():
    # [OBS, MOVES]
    training_data = []
    # all scores:
    scores = []
    # just the scores that met our threshold:
    accepted_scores = []
    # iterate through however many games we want:
    for _ in range(initial_games):
    	game.reset( False )
        score = 0
        # moves specifically from this environment:
        game_memory = []
        # for each frame in 200
        prev_observation = []
        alive = True
        while(True):
            # choose random action (0 or 1)
            action = game.sample()
            # do it!
            observation, reward, alive = game.step(action)
            if not alive:
                break

            # notice that the observation is returned FROM the action
            # so we'll store the previous observation here, pairing
            # the prev observation to the action we'll take.
            if len(prev_observation) > 0 :
                game_memory.append([prev_observation, action])
            prev_observation = observation
            score+=reward

        # IF our score is higher than our threshold, we'd like to save
        # every move we made
        # NOTE the reinforcement methodology here. 
        # all we're doing is reinforcing the score, we're not trying 
        # to influence the machine in any way as to HOW that score is 
        # reached.
        if score >= score_requirement:
            accepted_scores.append(score)
            for data in game_memory:
                # convert to one-hot (this is the output layer for our neural network)
                if data[1] == 0:
                    output = [1,0,0,0]
                elif data[1] == 1:
                    output = [0,1,0,0]
                elif data[1] == 2:
                	output = [0,0,1,0]
                elif data[1] == 3:
                	output = [0,0,0,1]
                    
                # saving our training data
                training_data.append([data[0], output])
        # save overall scores
        scores.append(score)
    
    # just in case you wanted to reference later
    training_data_save = np.array(training_data)
    np.save('saved.npy',training_data_save)
    
    # some stats here, to further illustrate the neural network magic!
    
    print('Average score:',mean(scores))
    print('Median score for scores:',median(scores))
    print(Counter(scores))
    #
    
    print('Average accepted score:',mean(accepted_scores))
    print('Median score for accepted scores:',median(accepted_scores))
    print(Counter(accepted_scores))
    #
    
    return training_data

def neural_network_model(input_size):

    network = input_data(shape=[None, input_size, 1], name='input')

    ##network = fully_connected(network, 36, activation='relu')
    ##network = dropout(network, 0.8)

    ##network = fully_connected(network, 1, activation='linear')
    ##network = dropout(network, 0.8)
    
    network = fully_connected(network, 512, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 128, activation='relu')
    network = dropout(network, 0.8)
    #

    network = fully_connected(network, 4, activation='softmax')
    network = regression(network, optimizer='adam', learning_rate=LR, loss='mean_square', name='targets')
    model = tflearn.DNN(network, tensorboard_dir='log')

    return model


def train_model(training_data, model=False):

    X = np.array([i[0] for i in training_data]).reshape(-1,len(training_data[0][0]),1)
    y = [i[1] for i in training_data]

    if not model:
        model = neural_network_model(input_size = len(X[0]))
    
    model.fit({'input': X}, {'targets': y}, n_epoch=7, snapshot_step=500, show_metric=True, run_id='openai_learning')
    return model

training_data = initial_population()
model = train_model(training_data)

scores = []
choices = []
for each_game in range(10):
    score = 0
    game_memory = []
    game.reset( True )
    win = game.getWindow()
    alive = True
    prev_obs = []
    new_observation = []
    while(True):
        win.getch()
        if len(prev_obs)==0:
            action = game.sample()
        else:
            action = np.argmax(model.predict(prev_obs.reshape(-1,len(prev_obs),1))[0])

        choices.append(action)
                
        new_observation, reward, alive = game.step(action)
        if not alive:
            break
        prev_obs = new_observation
        game_memory.append([new_observation, action])
        score+=reward
        #break
    game.close()
    scores.append(score)

print('Average Score:',sum(scores)/len(scores))
print('choice 1:{}  choice 0:{}'.format(choices.count(1)/len(choices),choices.count(0)/len(choices)))
print(score_requirement)
#"""
"""
game.reset( True )
win = game.getWindow()
key = KEY_RIGHT
alive = True
while key != 27 and alive:
	prevKey = key
	event = -1
	if win != None:												  # Previous key pressed
		event = win.getch()
	key = key if event == -1 else event 


	if key == ord( ' ' ):											# If SPACE BAR is pressed, wait for another
		key = -1												   # one (Pause/Resume)
		while key != ord( ' ' ):
			key = win.getch()
		key = prevKey
		continue

	if key not in [ KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27 ]:	 # If an invalid key is pressed
		key = prevKey

	action = 0
	if key == KEY_UP:
		action = 0
	elif key == KEY_RIGHT:
		action = 1
	elif key == KEY_DOWN:
		action = 2
	elif key == KEY_LEFT:
		action = 3

	state, reward, alive = game.step( action )
	#print alive"""

#print state