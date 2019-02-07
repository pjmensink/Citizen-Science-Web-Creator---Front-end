import json
numInputs = input('Number of inputs: ')
with open('data.json', 'w') as outfile:
	inputs = []
	for i in range(int(numInputs)):
		inputName = input('Enter name of input ' + str(i+1) + ': ')
		data = ({'key': inputName, 'label': inputName, 'name': inputName})
		inputs.append(data)
	json.dump(inputs, outfile)

