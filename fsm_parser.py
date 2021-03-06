# Need to make sure that no inputs, outputs, or states share the same names.
# It's not enough to make sure that each input is unique, each output is unique, etc,
# becaue Verilog doesn't allow reusing the same symbol even for different types of things.
def parse_fsm(source):
	inputs = {}
	outputs = {}
	states = {}
	for line in source:
		if line[0:len("define inputs =")] == "define inputs =":
			clipped_line = line[len('define inputs ='):]
			clipped_line.strip()
			# remove parentheses from clipped_line
			while len(clipped_line) > 0:
				if clipped_line.find(',') < 0:
					new_symbol = clipped_line
					clipped_line = ''
				else:
					new_symbol = clipped_line[0:clipped_line.find(',')]
					clipped_line = clipped_line[clipped_line.find(','):]
				if new_symbol in inputs.keys:
					# error message
					pass
				else:
					inputs[new_symbol] = 1 # default input size
		elif line[0:len('define outputs =')] == 'define outputs =':
			clipped_line = line[len('define outputs ='):]
			clipped_line.strip()
			# remove parentheses from clipped_line
			while len(clipped_line) > 0:
				if clipped_line.find(',') < 0:
					new_symbol = clipped_line
					clipped_line = ''
				else:
					new_symbol = clipped_line[0:clipped_line.find(',')]
					clipped_line = clipped_line[clipped_line.find(','):]
				if new_symbol in inputs.keys:
					# error message
					pass
				else:
					inputs[new_symbol] = 1 # default input size
		elif line[0:len("define state")] == "define state":
			clipped_line = line[len('define state'):]
			clipped_line.strip()
			new_symbol = clipped_line[0:clipped_line.find(' ')]
			clipped_line = clipped_line[len(new_symbol):]
			clipped_line.strip()
			clipped_line = clipped_line[1:] # remove equals sign
			clipped_line.strip()
			my_stack = []
			while len(clipped_line) > 0:
				if clipped_line[0] == '(':
					my_stack.push(clipped_line[0])
					clipped_line = clipped_line[1:]
				
		
		else:
			if (len(line) > 0):
				print "ERROR: Invalid source line"

	return [inputs, outputs, states]

# match any number of comma-separated inputs, with the requirement that each input name starts 
# with an alphanumeric character.
re.match("^define[ ]+inputs[ ]*=([A-Za-z].[A-Za-z0-9]*[ ]*[,[ ]*[A-Za-z0-9].[A-Za-z0-9]*[ ]*]*);")

# matches one and only one state specified as input state.
re.match("^define[ ]+init[ ]*=[ ]*[A-Za-z].[A-Za-z0-9]*[ ]*;")

def tabs(num_tabs):
	text = ""
	if (num_tabs <= 0):
		return ""
	for i in range(0, num_tabs):
		text += "\t"
	return text

def generate_verilog(inputs, outputs, states):
	my_verilog = [] # going to produce verilog as a list of strings, each string representing a line
	# generate module header
	#my_verilog.append("module
	# declare module inputs and outputs
	leading_tabs = 1
	my_verilog.append(tabs(leading_tabs) + "reg [{0}:0] state;".format(len(states)-1))
	next_line = "tabs(leading_tabs) + parameter " # "parameter sA = 2'b0, sB = 2'b1, etc" line
	for each in range(0, len(states)):
		if i == len(states)-1:
			next_line += "{0} = {1}b{2};".format(each[0], len(states)-1, i)
		else:
			next_line += "{0} = {1}b{2},".format(each[0], len(states)-1, i)
	my_verilog.append(next_line)

	my_verilog.append(tabs(leading_tabs) + "always @(posedge clock or negedge reset) begin")
	leading_tabs += 1
	my_verilog.append(tabs(leading_tabs) + "if(reset)")
	leading_tabs += 1
	my_verilog.append(tabs(leading_tabs) + "state <= init;")
	leading_tabs -= 1
	my_verilog.append(tabs(leading_tabs) + "else")
	leading_tabs += 1
	my_verilog.append(tabs(leading_tabs) + "state <= next_state;")
	leading_tabs -= 2
	my_verilog.append(tabs(leading_tabs) + "end")
	my_verilog.append("")		# want an empty line between always blocks
	
	next_line = "always @(state or "
	for i in range(0, len(inputs)):
		next_line += inputs[i]
		if i < len(inputs):
			next_line += " or "
	next_line += ") begin"
	my_verilog.append(next_line)
	leading_tabs = 3
	my_verilog.append(tabs(leading_tabs) + "case(state)")
	leading_tabs += 1
	for each in states:
		my_verilog.append(tabs(leading_tabs) + each[0] + ": begin")
		leading_tabs += 1
		# set output for this state
		# state transition logic
		# decrease leading_tabs
	# leading_tabs should be 2 at this point
	my_verilog.append(tabs(leading_tabs) + "endcase")
	leading_tabs -= 1
	my_verilog.append(tabs(leading_tabs) + "end")
	leading_tabs -= 1
	my_verilog.append(tabs(leading_tabs) + "endmodule")
	return my_verilog

# cleans up the user source code, changing tabs to spaces, multiple spaces to single ones, putting each statement on
# one and only one line.
def sanitize_source_code(source):
	source = source.replace('\t', ' ') # replace tabs with spaces
	# newline handling
  return source

def main():
	# load data
	# split lines into individual items in a list
	processed_stuff = parse_fsm(santize_souce_code(source))
