#! python3
# Arithmetic exercises

import pyinputplus as pyip
import re, time, random, sys
import logging as l

program_start_time = time.time()
l.basicConfig(level=l.DEBUG, 
    format='    %(levelname)s %(lineno)d, %(funcName)s - %(message)s')
l.disable(l.CRITICAL)

class Set_settings:
    """
    Set 1.rounds; 2.timer; 3.operators; 4.digit_length
    """
    l.debug('Entered Set_settings class.')

    def __init__(self):
        """
        Initialize. Get all the settings and return.
        """

        l.debug('Create settings variables in __init__.')
        
        self.rounds = self.create_rounds()
        self.timer = self.create_timer()
        self.operators = self.create_operator()
        self.max_digit = self.create_digit_length()
        
        l.debug('Exiting __init__')
        l.info(f'Program running time: {time.time() - program_start_time}')
        return None

    def create_rounds(self):
        """
        ROUNDS
        """
        l.debug('ROUNDS setting')

        # Ask for the number of how many excercises should be
        l.debug('Asking user input (inputInt)...')
        rounds = pyip.inputInt('How many rounds do you want (default is 10): ',  
                                blank=True,)

        l.debug(f'Input: {rounds}, which is {type(rounds)}')
        rounds = rounds or 10
        l.debug(f'After checking, rounds: {rounds}, which is {type(rounds)}')

        # Rounds should be int
        try:
            assert type(rounds) == int
        except Exception as x:
            l.critical(f'Assert exception. rounds var is not int', exc_info=True)
            sys.exit()
        return rounds

    def create_timer(self):
        """
        TIMEOUT
        """
        l.debug('TIMEOUT setting')

        # Ask if you want timeout
        l.debug('Asking user input (inputMenu)...')
        timer = pyip.inputMenu(['Yes', 'No'], 
                                numbered=True, 
                                prompt='Do you want to turn on timeout? (default is no)\n', 
                                blank=True)
        l.debug(f'User input (timer): {timer}')
        timer = timer or 'No'
        l.debug(f'After checking, timer: {timer}')
        l.debug(f'Match-case: if "timer" is "no", it is None; if "Yes", ask how many seconds.')
        match timer:
            case 'No':
                timer = None
            case 'Yes':
                timer = pyip.inputInt('How many seconds? ')
        l.debug(f'Timer after match-case: {timer} - {type(timer)}')
        return timer

    def create_operator(self):
        """
        OPERATOR
        """
        l.debug('OPERATOR setting')
        
        # Ask for the operator(s)
        l.debug('Creating regular expression:')
        re_operators = re.compile(r'^[*/+-]+$')
        l.debug(re_operators)
        print('Operators (*,/,-,+, default is any): ', end='')
        while True:
            l.debug('User input (python default input)...')
            operators = input()
            l.debug(f'User input: {operators}')
            # If input is blank, include all operators
            operators = operators or '*/-+'
            l.debug(f'User input after checking: {operators}')
            l.debug('Running operators agains regex.')
            if re.search(re_operators, operators) == None:
                l.debug("Regex didn't match \"operators\"")
                print('Invalid input')
                continue
            l.debug(f'Found match: {re_operators.search(operators).group()}')
            l.debug(f'Converting operators ({type(operators)}): {operators} to list.')
            # unpacking: [*operators]
            operators = list(operators)
            l.debug(f'Converted successfully: {operators}')
            break
        return operators

    def create_digit_length(self):
        """
        DIGIT LENGTH
        """
        l.debug('DIGIT LENGTH setting.')

        # How many digits the numbers have
        l.debug('Getting user input (inputMenu)...')
        digit_length = pyip.inputMenu(['2', '3', '4', '5', '6', '7', '8'], 
                                        'How long is the max number?\n')
        l.debug(f'User input: {digit_length}')
        l.debug('Creating max_digit...')
        try:
            max_digit = int('9'*int(digit_length))
        except:
            l.critical('Failed to create digit_length. Exiting...')
            sys.exit()
        else:
            l.debug(f'Created successfully. max_digit: {max_digit} type: {type(max_digit)}')    
        return max_digit


def run():
    """
    Run arithmetic excercises based on the settings
    """
    l.debug('Entered run()')

    # Total duration
    start_time = time.time()
    l.debug(f'Function begins at {start_time}')
    # Keep track of everyting
    results = []
    correct_count = 0
    timeout_count = 0

    for r in range(settings.rounds):
        debug_round_count = r+1
        l.debug(f'Beginning of round {debug_round_count}')
        # One exercise duration
        round_start_time = time.time()
        l.debug(f'Loop {debug_round_count} starts at {round_start_time}')

        # Create variables
        l.debug(f'Creating excercise for round {debug_round_count}...')
        try:
            num1 = random.randint(1, settings.max_digit)
            num2 = random.randint(1, settings.max_digit)
            operator = random.choice(settings.operators)
        except:
            l.error(f'Failed to create. Round {debug_round_count}.' + 
                        f'Vars: {num1, num2, operator}')
            continue
        else:
            l.debug(f'Created successfully: {num1, operator, num2}')
        real_answer = 0
        
        # Calculate the answer
        match operator:
            case '*':
                real_answer = num1 * num2
            case '/':
                if num1 < num2:
                    num1, num2 = num2, num1
                real_answer = num1 / num2
            case '-':
                real_answer = num1 - num2
            case '+':
                real_answer = num1 + num2
        real_answer = float(real_answer)
        real_answer = round(real_answer, 1)
        
        print(f'\n-----{r+1}-----')
        is_timeout = False
        l.debug('Created is_timeout. Set to False')
        # 2 tries to answer
        for i in range(2):
            # User answer
            l.debug('Answer stopwatch has set off.')
            answer_time = time.time()
            while True:
                # Only a number is accepted
                try:
                    l.debug('Try')
                    l.debug('User input, should be a number because of float()...')
                    answer = None
                    answer = float(input(f'{num1} {operator} {num2} = '))
                except:
                    l.debug(f'Exception. Input: {answer}; Type: {type(answer)}')
                    print('It should be a number. Try again.')
                    continue
                else:
                    l.debug('Else')
                    l.debug('Checking if timeout is reached:')
                    l.debug(f'({time.time()} - {answer_time}) > {settings.timer}: {is_timeout}')
                    if settings.timer:
                        is_timeout = (time.time() - answer_time) > settings.timer
                    l.debug(f'is_timeout: {is_timeout}')
                    l.debug(f'Input {answer} has been accepted.')
                    break

            # Check user answer
            l.debug(f'Correct answer: {real_answer}; User answer: {answer}')
            is_correct = float(real_answer) == answer
            l.debug(f'They are equal: {is_correct}')

            # Compare user and real answers
            l.debug(f'is_correct={is_correct}. Match-case...')
            match is_correct:
                case True:
                    correct_count += 1
                    if not is_timeout:
                        l.debug('match-case: True. (correct) and is_timeout=False')
                        print('CORRECT!')
                    else:
                        l.debug('match-case: True (correct) but is_timeout=True')
                        print('CORRECT. But time was up.')
                        timeout_count += 1
                    break
                case False:
                    l.debug(f'match-case: False. {i+1}/2')
                    print(f'INCORRECT. {i+1}/2')
        
        # Calculate the round duration
        time_took = time.time() - round_start_time
        l.debug(f'It took {time.time()} - {round_start_time} = {time_took}')
        l.debug(f'time_took type: {type(time_took)}')
        l.debug(f'Rounding...')
        try:
            time_took = round(time_took)
        except Exception as x:
            l.error('Rounding has failed', exc_info=True)
            try:
                l.debug(f'Converting to int: {time_took} -> {int(time_took)}')
                time_took = int(time_took)
            except:
                l.error('Converting to int has failed', exc_info=True)
        else:
            l.debug(f'Successfully rounded: {time_took}')
        
        print(f'> Answer: {real_answer} | {time_took} sec')
        
        
        l.debug('Appending "results" list.')
        results.append({
            'count': r+1,
            'exercise': f'{num1}{operator}{num2}',
            'real_answer': real_answer,
            'user_answer': answer,
            'timer': time_took,
        })
        l.debug(results)

        l.debug(f'Loop {debug_round_count} is finished. ')
        l.info(f'Program running time: {time.time() - program_start_time}')

    
    print_overview(results, correct_count, timeout_count)


def print_overview(results, correct_count, timeout_count):
    """
    Build an overview table
    """
    l.debug('Entered "print_overview" function')
    
    
    print('='*20)
    # Settings table
    space_count = 4
    l.debug(f'settings.timer = {settings.timer}. If None, convert to 0')
    timer_sec = settings.timer or 0
    l.debug(f'settings.timer after checking: {timer_sec}')

    print('SETTINGS -')
    print('rounds'.ljust(9) + ' '*space_count + str(settings.rounds))
    print('timer'.ljust(9) + ' '*space_count + str(timer_sec) + 's')
    print('operators'.ljust(9) + ' '*space_count + ''.join(settings.operators))
    print('max digit'.ljust(9) + ' '*space_count + str(settings.max_digit))

    print('='*20)
    # Results table
    print('RESULTS -')
    print(
	'#'.ljust(4) +
	'Exercise'.ljust(10) +
	' ' +
	'Correct'.rjust(10) +
	'   ' +
	'Yours' +
	'   ' +
	'Secs'
    )
    for r in results:
        print(
            str(r['count']).ljust(4) +
            str(r['exercise']).ljust(10) +
            ' ' +
            str(r['real_answer']).rjust(10) +
            '   ' +
            str(r['user_answer']) +
            '   ' +
            str(r['timer']) + 's'
        )

    # Correct, Timeout
    print(f'Correct: {correct_count}')
    print(f'Timeout: {timeout_count}')


if __name__=='__main__':
    settings = Set_settings()
    run()
    



"""
====================
SETTINGS - 
rounds      3
timer       10s
operators   +
max digit   99
====================
RESULTS -
1   2+2   4   4   3sec
2   5+3   8   9   6sec
3   9+1   10  11  14sec
correct: 1
timeout: 1
"""


