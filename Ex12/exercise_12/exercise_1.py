from fuzzingbook.Grammars import Grammar, crange, is_valid_grammar, opts
from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from fuzzingbook.ProbabilisticGrammarFuzzer import ProbabilisticGrammarFuzzer
from fuzzingbook.GeneratorGrammarFuzzer import GeneratorGrammarFuzzer, ProbabilisticGeneratorGrammarCoverageFuzzer
from fuzzingbook.WebFuzzer import WebFormFuzzer, HTMLGrammarMiner, cgi_encode

manipulated_values = {
    'manipulated_name': False,
    'manipulated_lastname': False,
    'manipulated_mail': False,
    'manipulated_password': False,
    'manipulated_password_short': False,
    'manipulated_password_long': False,
    'manipulated_password2': False
}

def manipulated(name, lastname, email, password, password2, banking):
    global manipulated_values
    if not manipulated_values['manipulated_name']:
        manipulated_values['manipulated_name'] = True
        name = '123'
    if not manipulated_values['manipulated_lastname']:
        manipulated_values['manipulated_lastname'] = True
        lastname = '123'
    if not manipulated_values['manipulated_password']:
        manipulated_values['manipulated_password'] = True
        password = 'password1'
        password2 = 'password1'
    elif not manipulated_values['manipulated_password2']:
        manipulated_values['manipulated_password2'] = True
        password2 = 'password1'
    elif all([manipulated_values['manipulated_name'], manipulated_values['manipulated_lastname'], manipulated_values['manipulated_password'], manipulated_values['manipulated_password2']]):
        if not manipulated_values['manipulated_password_short']:
            manipulated_values['manipulated_password_short'] = True
            password = cgi_encode("pa!")
            password2 = cgi_encode("pa!")
        elif not manipulated_values['manipulated_password_long']:
            manipulated_values['manipulated_password_long'] = True
            password = cgi_encode('pass!' * 5)
            password2 = cgi_encode('pass!' * 5)
        elif not manipulated_values['manipulated_mail']:
            manipulated_values['manipulated_mail'] = True
            email = email + '.saarland'

    return requesting(name, lastname, email, password, password2, banking)

def requesting(name, lastname, email, password, password2, banking):
    request_params = {
        'name': name,
        'lastname': lastname,
        'email': email,
        'password': password,
        'password2': password2,
        'banking': banking
    }
    
    request_str = "/register?"
    for key, value in request_params.items():
        request_str += f"{key}={value}&"
    
    # Removing the trailing '&' if it exists
    if request_str.endswith('&'):
        request_str = request_str[:-1]
    
    return request_str
    
def check_sum(digits):
    from luhn import luhn
    calculated_sum = luhn(digits[:-1])
    return digits[:-1] + str(calculated_sum)

REGISTRATION_GRAMMAR: Grammar = {
    "<start>": ["<registration>"],
    "<registration>": [("/register?name=<name>&lastname=<lastname>&email=<email>"
                       "&password=<password>&password2=<password2>&banking=<banking>",
                      opts(post=manipulated))],
    "<name>": ["Leon", "Marius"],
    "<lastname>": ["Bettscheider", "Smytzek"],
    "<email>": [cgi_encode("leon.bettscheider@cispa.de"), 
                cgi_encode("marius.smytzek@cispa.de")],
    "<password>": [cgi_encode("password!")],
    "<password2>": [cgi_encode("password!")],
    "<banking>": [("<digits>", opts(post=check_sum))],
    "<digits>": ["<digit><digit><digit><digit><digit><digit><digit><digit><digit><digit><digit><digit><digit><digit><digit><digit>"],
    "<digit>": crange('0', '9')
}

assert is_valid_grammar(REGISTRATION_GRAMMAR)

def get_fuzzer(httpd_url):
    return GeneratorGrammarFuzzer(REGISTRATION_GRAMMAR)