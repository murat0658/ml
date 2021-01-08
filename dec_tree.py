import random
from math import log
import datetime


def _calculate_entropy(count, total, base):
	probability = 0
	if(total != 0 and count != 0):
		probability = float(count)/total
		return -probability * log(probability, base)
	else:
		return 0

def calculate_entropy(counts):
	total = sum(counts)
	base = int(len(counts))
	entropy_of_classes = 0
	for count in counts:
		entropy_of_classes += _calculate_entropy(count, total, base)
	return entropy_of_classes

file  = "car.data"
def get_file_data_as_matrix():
	with open(file, 'r') as fd:
		data = fd.read()
	data_list = data.split('\n')
	data_list = data_list[:-1]
	random.shuffle(data_list) 
	# columns: buying, maint , doors, persons, lug_boot, safety respectively
	data_matrix = [el.split(',') for el in data_list]
	return data_matrix

all_attr_vals = [
		['vhigh', 'high', 'med', 'low'], # buying
		['vhigh', 'high', 'med', 'low'], # maint
		['2', '3', '4', '5more'], # doors
		['2', '4', 'more'], # persons
		['small', 'med', 'big'], #lug_boot
		['low', 'med', 'high'] # safety
	]

class_vals = ['unacc', 'acc', 'good', 'vgood']

def get_class_counts_per_data_matrix():
	all_attr_counts = [[[0 for k in range(CLASS_COUNT)] for j in range(i)] for i in number_of_attrs]

	for attrs in training_data_matrix:
		class_data = attrs[-1] # ex: unacc
		# class counts only:
		for i in range(CLASS_COUNT):
			class_val = class_vals[i]
			if class_data == class_val:
				class_counts[i] += 1
		for i in range(NUM_OF_ATTRS):
			attr = attrs[i] # ex: vhigh
			attr_vals = all_attr_vals[i] # ex: ['vhigh', 'high', 'med', 'low'], # buying
			index_of_attr = attr_vals.index(attr) # 0 in this case	
			for j in range(CLASS_COUNT): 
				if(class_vals[j] == class_data):
					all_attr_counts[i][index_of_attr][j] += 1
					break
	return all_attr_counts

def calculate_gain_ratios(entropies_per_attr, counts_per_attr, class_entropies):
	gain_ratios = [0] * NUM_OF_ATTRS
	for i in range(NUM_OF_ATTRS):
		entropies = entropies_per_attr[i]
		counts = counts_per_attr[i]
		lst_size = number_of_attrs[i]
		entropy = 0
		split_info = 0
		for j in range(lst_size):
			if(counts[j] != 0 and lst_size != 0):
				probability = float(counts[j])/training_data_length
				entropy += probability * entropies[j]
				split_info += - probability * log(probability, lst_size)
		gain = class_entropies - entropy
		if(split_info == 0):
			gain_ratios[i] = 0
		else:
			gain_ratios[i] = gain / split_info
	return gain_ratios

def calculate_global_entropy():
	return calculate_entropy(class_counts)

def calculate_all_entropies_of_attributes(all_attr_counts):
	entropies_of_attrs = [[0 for y in range(i)] for i in number_of_attrs]
	number_of_entries = [[0 for y in range(i)] for i in number_of_attrs]
	for i in range(NUM_OF_ATTRS):
		attr_counts = all_attr_counts[i]
		for j in range(number_of_attrs[i]):
			attr_counts_per_class = attr_counts[j]
			total = sum(attr_counts_per_class)
			number_of_entries[i][j] = total
			entropies_of_attrs[i][j] = calculate_entropy(attr_counts_per_class)
	return (number_of_entries, entropies_of_attrs)
	for lst in number_of_entries:
		assert(sum(lst) == training_data_length )

def is_homogeneous(data_matrix):
	class_val = data_matrix[0][-1]
	for el in data_matrix:
		if(el[-1] != class_val):
			return False
	return True

def create_decision_tree(data_matrix, index):
	data_list = [row[index] for row in data_matrix]
	data_vals = all_attr_vals[index]
	tree = []
	temp_data_matrix = data_matrix[index+1:]
	for i in range(len(data_vals)):
		data_val = data_vals[i]
		new_data_matrix = [data_matrix[j] for j, x in enumerate(data_list) if x == data_val]
		if(new_data_matrix != []):
			if(index == prun_level):
				dominant_class_index = all_attr_counts[prun_level][i].index(max(all_attr_counts[prun_level][i]))
				tree.append({data_val: class_vals[dominant_class_index]})
			elif(is_homogeneous(new_data_matrix)):
				tree.append({data_val: new_data_matrix[0][-1]})
			else:
				tree.append({data_val: create_decision_tree(new_data_matrix, index+1)}) 
	if(tree == []):
		return None
	return tree

def change_order_of_data_matrix_and_data_values():
	new_data_matrix = []
	new_test_data_matrix = []
	new_all_attr_vals = []
	new_all_attr_counts = []
	for i in range(NUM_OF_ATTRS):
		index = gain_ratios.index(max(gain_ratios))
		new_all_attr_vals.append(all_attr_vals[index]) 
		new_all_attr_counts.append(all_attr_counts[index])
		if(new_data_matrix == []):
			new_data_matrix = [[training_data_matrix[j][index]] for j in range(training_data_length)]
			new_test_data_matrix = [[test_data_matrix[j][index]] for j in range(test_data_length)]
		else:
			new_data_matrix = [new_data_matrix[j] + [training_data_matrix[j][index]] for j in range(training_data_length)]
			new_test_data_matrix = [new_test_data_matrix[j] + [test_data_matrix[j][index]] for j in range(test_data_length)]
		gain_ratios[index] = -1
	new_data_matrix =[new_data_matrix[j] + [training_data_matrix[j][-1]] for j in range(training_data_length)]# class labels
	new_test_data_matrix = [new_test_data_matrix[j] + [test_data_matrix[j][-1]] for j in range(test_data_length)]
	return (new_data_matrix, new_all_attr_vals, new_test_data_matrix, new_all_attr_counts)

def test_instance_against_tree(tree, instance):
	if(type(tree) == str):
		if(tree == instance[-1]):
			return True
		else:
			return False
	else:
		for node in tree:
			attr = instance[0]
			if(attr in node):
				return test_instance_against_tree(node[attr], instance[1:])
		return False

def test_model(tree):
	counter = 0
	for instance in test_data_matrix:
		if(test_instance_against_tree(tree, instance)):
			counter += 1
	return str((float(counter) / test_data_length) *100) + "%"

start_time = datetime.datetime.now() ;
print("starting...\n")

NUM_OF_ATTRS = 6
CLASS_COUNT = 4

NUM_OF_BUYING_ATTR = 4
NUM_OF_MAINT_ATTR = 4
NUM_OF_DOORS_ATTR = 4
NUM_OF_PERSONS_ATTR = 3
NUM_OF_LUG_BOOT_ATTR = 3
NUM_OF_SAFETY_ATTR = 3

number_of_attrs = [
	NUM_OF_BUYING_ATTR,
	NUM_OF_MAINT_ATTR,
	NUM_OF_DOORS_ATTR,
	NUM_OF_PERSONS_ATTR,
	NUM_OF_LUG_BOOT_ATTR,
	NUM_OF_SAFETY_ATTR
]

class_counts = [0] * CLASS_COUNT # "unacc, acc, good, vgood" respectively



data_matrix = get_file_data_as_matrix()
# splitting data to training and test 
training_data_length = int(len(data_matrix) * 2 / 3)
test_data_length = len(data_matrix) - training_data_length
training_data_matrix = data_matrix[:training_data_length]
test_data_matrix = data_matrix[training_data_length:]
# all_attr_counts : 3D matrix data matrix 
# 1st dim. : attributes
# 2nd dim. : attr values
# 3rd dim. : class counts
all_attr_counts = get_class_counts_per_data_matrix()
# entropy_of_classes: global entropy of dara
entropy_of_classes = calculate_global_entropy()
# number_of_entries: summation of 3rd dimension of all_attr_counts, so 2D.
# gives attr value counts per attribute. calculated for easiness
# entropies_of_attrs: gives entropies of attr values
# according to "attr value class" labels
(number_of_entries, entropies_of_attrs) = calculate_all_entropies_of_attributes(all_attr_counts)
gain_ratios = calculate_gain_ratios(entropies_of_attrs, number_of_entries, entropy_of_classes)
(training_data_matrix, all_attr_vals, test_data_matrix, all_attr_counts) = change_order_of_data_matrix_and_data_values()
for prun_level in range(NUM_OF_ATTRS):
	tree = create_decision_tree(training_data_matrix, 0)
	accuracy = test_model(tree)
	print("prunned tree in level " + str(prun_level+1) + "\n")
	print("time " +str((datetime.datetime.now() -start_time).total_seconds() )+ "seconds\n")
	print("tree "+ str(tree) + "\n")
	print("accuracy "  + accuracy)
	print("\n\n\n")
