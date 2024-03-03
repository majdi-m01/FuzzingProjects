import string
from fuzzingbook.Grammars import srange, is_valid_grammar

HTML_GRAMMAR = {
    '<start>': ['<doctype><html>'],
    '<doctype>': ['<lt>!DOCTYPE html<gt>', # html5
                  '<lt>!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"<gt>', # html4
                  '<lt>!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"<gt>', # html3
                 ],
    '<html>': ['<head><body>'],
    '<head>': ['<lt>head<gt><header_content><lt>/head<gt>'],
    '<body>': ['<lt>body<gt><body_content><lt>/body<gt>'],
    '<header_content>': ['',
                         '<title><header_content>',
                         '<meta><header_content>'],
    '<title>': ['<lt>title<gt><title_content><lt>/title<gt>'],
    '<title_content>': ['', '<title_char><title_content>'],
    '<title_char>': srange(string.ascii_letters + string.digits + "',-_ "),
    '<meta>': ['<lt>meta <meta_attributes><gt>'],
    '<meta_attributes>': ['charset="UTF-8"',  'name="author" content="<author>"'],
    '<author>': ['<chars>'],
    '<body_content>': ['',
                       '<div><body_content>', 
                       '<p><body_content>', 
                       '<ul><body_content>', 
                       '<ol><body_content>', 
                       '<text><body_content>'],
    '<div>': ['<lt>div<gt><body_content><lt>/div<gt>'],
    '<p>': ['<lt>p<gt><text><lt>/p<gt>'],
    '<ul>': ['<lt>ul<gt><list><lt>/ul<gt>'],
    '<ol>': ['<lt>ol<gt><list><lt>/ol<gt>'],
    '<list>': ['', '<lt>li<gt><body_content><lt>/li<gt><list>'],
    '<lt>': ['<'],
    '<gt>': ['>'],
    '<br>': ['<lt>br<gt>'],
    '<text>': ['', '<chars><br><text>'],
    '<chars>': ['', '<char><chars>'],
    '<char>': srange(string.printable),
}

assert is_valid_grammar(HTML_GRAMMAR)