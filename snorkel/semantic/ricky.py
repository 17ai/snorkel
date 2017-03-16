from __future__ import print_function

from pdb import set_trace as t
from grammar import Rule

# Helpers ======================================================================
def sems0(sems):
    return sems[0]

def sems1(sems):
    return sems[1]

def sems_in_order(sems):
    return tuple(sems)

def sems_reversed(sems):
    return tuple(reversed(sems))

# Rules ======================================================================
lexical_rules = (
    # [Rule('$Start', w) for w in ['<START>']] +
    # [Rule('$Stop', w) for w in ['STOP']] +
    [Rule('$Label', w, '.label') for w in ['label ?it']] +
    [Rule('$Arg', w, '.arg') for w in ['arg', 'argument']] +
    [Rule('$True', w, ('.bool', True)) for w in ['true', 'correct']] +
    [Rule('$False', w, ('.bool', False)) for w in ['false', 'incorrect', 'wrong']] +
    [Rule('$And', w, '.and') for w in ['and']] +
    [Rule('$Or', w, '.or') for w in ['or', 'nor']] +
    [Rule('$Not', w, '.not') for w in ['not', "n't"]] +
    [Rule('$All', w, '.all') for w in ['all']] +
    [Rule('$Any', w, '.any') for w in ['any', 'a']] +
    [Rule('$None', w, '.none') for w in ['none', 'not any', 'neither', 'no']] +
    # [Rule('$Is', w) for w in ['is', 'are', 'be']] +
    [Rule('$Because', w) for w in ['because', 'since', 'if']] +
    [Rule('$Upper', w, '.upper') for w in ['upper', 'uppercase', 'upper case', 'all caps', 'all capitalized']] +
    [Rule('$Lower', w, '.lower') for w in ['lower', 'lowercase', 'lower case']] +
    [Rule('$Capital', w, '.capital') for w in ['capital', 'capitals', 'capitalized']] +
    [Rule('$Equals', w, '.eq') for w in ['equal', 'equals', '=', '==', 'same', 'identical', 'exactly']] + 
    [Rule('$LessThan', w, '.lt') for w in ['less than', 'smaller than', '<']] +
    [Rule('$AtMost', w, '.leq') for w in ['at most', 'no larger than', 'less than or equal', 'within', 'no more than', '<=']] +
    [Rule('$AtLeast', w, '.geq') for w in ['at least', 'no less than', 'no smaller than', 'greater than or equal', '>=']] +
    [Rule('$MoreThan', w, '.gt') for w in ['more than', 'greater than', 'larger than', '>']] + 
    [Rule('$Within', w, '.within') for w in ['within']] +
    [Rule('$Exists', w) for w in ['exist', 'exists', 'there']] +
    [Rule('$Int', w, ('.int', 0)) for w in ['no']] +
    [Rule('$Int', w,  ('.int', 1)) for w in ['immediately']] +
    # Rule('$AtLeastOne', 'a', ('.geq', ('.int', 1))),
    # Rule('$Int', 'a', ('.int', 1)),
    [Rule('$In', w, '.in') for w in ['in']] +
    [Rule('$Contains', w, '.contains') for w in ['contains', 'contain']] +
    [Rule('$StartsWith', w, '.startswith') for w in ['starts with', 'start with']] +
    [Rule('$EndsWith', w, '.endswith') for w in ['ends with', 'end with']] +
    [Rule('$Left', w, '.left') for w in ['left', 'before', 'precedes', 'preceding', 'followed by']] +
    [Rule('$Right', w, '.right') for w in ['right', 'after', 'follows', 'following']] +
    [Rule('$Sentence', w, '.sentence') for w in ['sentence', 'in the sentence']] +
    [Rule('$Between', w, '.between') for w in ['between', 'inbetween']] +
    [Rule('$Separator', w) for w in [',', ';', '/']] +
    [Rule('$Count', w, '.count') for w in ['number', 'length', 'count']] +
    [Rule('$Word', w, 'words') for w in ['word', 'words', 'term', 'terms', 'phrase', 'phrases']] + 
    [Rule('$Char', w, 'chars') for w in ['character', 'characters', 'letter', 'letters']] + 
    [Rule('$NounPOS', w, ('.string', 'NN')) for w in ['noun', 'nouns']] +
    [Rule('$DateNER', w, ('.string', 'DATE')) for w in ['date', 'dates']] +
    [Rule('$NumberPOS', w, ('.string', 'CD')) for w in ['number', 'numbers']] +
    [Rule('$PersonNER', w, ('.string', 'PERSON')) for w in ['person', 'people']] +
    [Rule('$LocationNER', w, ('.string', 'LOCATION')) for w in ['location', 'locations', 'place', 'places']] +
    [Rule('$OrganizationNER', w, ('.string', 'ORGANIZATION')) for w in ['organization', 'organizations']] +
    [Rule('$Punctuation', w) for w in ['.', ',', ';', '!', '?']] +
    [Rule('$Tuple', w, '.tuple') for w in ['pair', 'tuple']] +
    # FIXME: Temporary hardcode
    [Rule('$ChemicalEntity', w, ('.string', 'Chemical')) for w in ['chemical', 'chemicals']] +
    [Rule('$DiseaseEntity', w, ('.string', 'Disease')) for w in ['disease', 'diseases']] +
    [Rule('$CID', w, '.cid') for w in ['cid', 'cids', 'canonical id', 'canonical ids']]
    # FIXME
)

unary_rules = [
    # FIXME: Temporary hardcode
    Rule('$ArgX', '$ChemicalEntity', ('.arg', ('.int', 1))),
    Rule('$ArgX', '$DiseaseEntity', ('.arg', ('.int', 2))),
    # FIXME
    Rule('$Bool', '$BoolLit', sems0),
    Rule('$BoolLit', '$True', sems0),
    Rule('$BoolLit', '$False', sems0),
    Rule('$Conj', '$And', sems0),
    Rule('$Conj', '$Or', sems0),
    # Rule('$Exists', '$Is'),
    # Rule('$Equals', '$Is', '.eq'),
    Rule('$Compare', '$Equals', sems0),
    Rule('$Compare', '$NotEquals', sems0),
    Rule('$Compare', '$LessThan', sems0),
    Rule('$Compare', '$AtMost', sems0),
    Rule('$Compare', '$MoreThan', sems0),
    Rule('$Compare', '$AtLeast', sems0),
    Rule('$WithIO', '$Within', sems0),
    Rule('$WithIO', '$Without', sems0),
    Rule('$Direction', '$Left', sems0),
    Rule('$Direction', '$Right', sems0),
    Rule('$POS', '$NounPOS', sems0),
    Rule('$POS', '$NumberPOS', sems0),
    Rule('$NER', '$DateNER', sems0),
    Rule('$NER', '$PersonNER', sems0),
    Rule('$NER', '$LocationNER', sems0),
    Rule('$NER', '$OrganizationNER', sems0),
    Rule('$Unit', '$Word', sems0),
    Rule('$Unit', '$Char', sems0),
    Rule('$StringList', '$UserList', sems0),
    Rule('$UnaryStringToBool', '$Lower', sems0),
    Rule('$UnaryStringToBool', '$Upper', sems0),
    Rule('$UnaryStringToBool', '$Capital', sems0),
    Rule('$BinaryStringToBool', '$StartsWith', sems0),
    Rule('$BinaryStringToBool', '$EndsWith', sems0),
    Rule('$BinaryStringToBool', '$In', sems0),
    Rule('$BinaryStringToBool', '$Contains', sems0),
    Rule('$BinaryStringToBool', '$Compare', sems0),
    Rule('$IntToBool', '$AtLeastOne', sems0),
    # ArgX may be treated as an object or a string (referring to its textual contents)
    Rule('$String', '$ArgX', lambda sems: ('.arg_to_string', sems[0])),
    Rule('$ArgToString', '$CID', lambda sems: (sems[0],)),
    Rule('$StringList', 'StringListOr', sems0),
    Rule('$StringList', 'StringListAnd', sems0),
    Rule('$List', '$BoolList', sems0),
    Rule('$List', '$StringList', sems0), # Also: UserList ->  StringList -> List
    Rule('$List', '$IntList', sems0),
    Rule('$List', '$TokenList', sems0),
    Rule('$ROOT', '$LF', lambda sems: ('.root', sems[0])),
]

compositional_rules = [
    # Rule('$ROOT', '$Start $LF $Stop', lambda sems: ('.root', sems[1])),
    Rule('$LF', '$Label $Bool $Because $Bool ?$Punctuation', lambda sems: (sems[0], sems[1], sems[3])),

    ### Logicals ###
    Rule('$Bool', '$Bool $Conj $Bool', lambda sems: (sems[1], sems[0], sems[2])),
    Rule('$Bool', '$Not $Bool', sems_in_order),
    Rule('$Bool', '$All $BoolList', sems_in_order),
    Rule('$Bool', '$Any $BoolList', sems_in_order),
    Rule('$Bool', '$None $BoolList', sems_in_order),
    
    # Parentheses
    Rule('$Bool', '$OpenParen $Bool $CloseParen', lambda (open_, bool_, close_): bool_),
    # Rule('$StringListAnd', '$OpenParen $StringListAnd $CloseParen', lambda (open_, list_, close_): list_),
    # Rule('$StringListOr', '$OpenParen $StringListOr $CloseParen', lambda (open_, list_, close_): list_),

    ### Strings ###
        # building strings
    Rule('$StringStub', '$Quote $QueryToken', lambda sems: [sems[1]]),
    Rule('$StringStub', '$StringStub $QueryToken', lambda sems: sems[0] + [sems[1]]),
    Rule('$String', '$StringStub $Quote', lambda sems: ('.string', ' '.join(sems[0]))),
    Rule('$String', '$Word $String', sems1),

        # building string lists (TODO: remove some redundancies here?)
    Rule('$StringList', '$String ?$Separator $String', lambda sems: ('.list', sems[0], sems[2])),
    Rule('$StringList', '$StringList ?$Separator $String', lambda sems: tuple((list(sems[0]) + [sems[2]]))),
    
    Rule('$StringListOr', '$String ?$Separator $Or $String', lambda sems: ('.list', sems[0], sems[3])),
    Rule('$StringListOr', '$StringList ?$Separator $Or $String', lambda sems: tuple(list(sems[0]) + [sems[3]])),

    Rule('$StringListAnd', '$String ?$Separator $And $String', lambda sems: ('.list', sems[0], sems[3])),
    Rule('$StringListAnd', '$StringList ?$Separator $And $String', lambda sems: tuple(list(sems[0]) + [sems[3]])),

        # applying $StringToBool functions
    Rule('$Bool', '$String $StringToBool', lambda sems: ('.call', sems[1], sems[0])),
    Rule('$Bool', '$String $Not $StringToBool', lambda (str_, not_, func_): (not_, ('.call', func_, str_))),
    Rule('$Bool', '$StringListOr $StringToBool', lambda sems: ('.any', ('.map', sems[1], sems[0]))),
    Rule('$Bool', '$StringListAnd $StringToBool', lambda sems: ('.all', ('.map', sems[1], sems[0]))),
    Rule('$BoolList', '$StringList $StringToBool', lambda sems: ('.map', sems[1], sems[0])),

        # defining $StringToBool functions
    Rule('$StringToBool', '$UnaryStringToBool', lambda sems: (sems[0],)),
    Rule('$StringToBool', '$BinaryStringToBool $String', sems_in_order),
    Rule('$StringToBool', '$In $StringList', sems_in_order),
    Rule('$StringToBool', '$BinaryStringToBool $StringListAnd', lambda sems: ('.composite_and', (sems[0],), sems[1])),
    Rule('$StringToBool', '$BinaryStringToBool $StringListOr', lambda sems: ('.composite_or',  (sems[0],), sems[1])),
    Rule('$StringToBool', '$BinaryStringToBool $UserList', lambda sems: ('.composite_or',  (sems[0],), sems[1])),
    
        # absorb redundancy
    Rule('$UserList', '$UserList $Word', sems0),
    Rule('$UserList', '$Word $UserList', sems1),

        # intersection
    # Rule('$List', '$StringList $In $StringList', lambda (list1, in_, list2): ('.intersection', list1, list2)),

    ### Integers ###
        # applying $IntoToBool functions
    Rule('$Bool', '$Int $IntToBool', lambda sems: ('.call', sems[1], sems[0])),
    Rule('$BoolList', '$IntList $IntToBool', lambda sems: ('.map', sems[1], sems[0])),
    Rule('$IntToBool', '$Compare $Int', sems_in_order),

        # flipping inequalities
    Rule('$AtMost', '$Not $MoreThan', '.leq'),
    Rule('$AtLeast', '$Not $LessThan', '.geq'),
    Rule('$LessThan', '$Not $AtLeast', '.lt'),
    Rule('$MoreThan', '$Not $AtMost', '.gt'),
    Rule('$NotEquals', '$Not $Equals', '.neq'),
    Rule('$NotEquals', '$Equals $Not', '.neq'), # necessary because 'not' requires a bool, not an IntToBool
    Rule('$Without', '$Not $Within', '.without'), # necessary because 'not' requires a bool, not an IntToBool
    
        # "more than five of X words are upper"
    Rule('$Bool', '$IntToBool $BoolList', lambda (func_,boollist_): ('.call', func_, ('.sum', boollist_))),

    ### Context ###
    Rule('$ArgX', '$Arg $Int', sems_in_order),
    Rule('$ArgXOr', '$ArgX $Or $ArgX', lambda (arg1_, and_, arg2_): ('.list', arg1_, arg2_)),
    Rule('$ArgXAnd', '$ArgX $And $ArgX', lambda (arg1_, and_, arg2_): ('.list', arg1_, arg2_)),

        # make lists
    Rule('$PhraseList', '$Direction $ArgX', lambda (dir_, arg_): (dir_, arg_)),
    Rule('$PhraseList', '$Between $ArgXAnd', lambda (btw_, arglist_): (btw_, arglist_)),
    Rule('$PhraseList', '$Sentence', lambda (sent,): (sent,)),

        # implicit 'in'
    # Rule('$StringToBool', '$StringAndArgToBool $ArgX', sems_in_order),
    # Rule('$StringToBool', '$StringAndArgToBool $ArgXOr', lambda sems: ('.composite_or', (sems[0],), sems[1])),
    # Rule('$StringToBool', '$StringAndArgToBool $ArgXAnd', lambda sems: ('.composite_and', (sems[0],), sems[1])),

            # "is left of Y"
    Rule('$StringToBool', '$Direction $ArgX',
        lambda (dir_, arg_): ('.in', ('.extract_text', (dir_, arg_)))),
            # "is two words left of Y"    
    Rule('$StringToBool', '$Int ?$Unit $Direction $ArgX', 
        lambda (int_, unit_, dir_, arg_): ('.in', ('.extract_text', 
            (dir_, arg_, ('.string', '.eq'), int_, ('.string', (unit_ if unit_ else 'words')))))),
            # "is at least 40 words to the left of"
    Rule('$StringToBool', '$Compare $Int ?$Unit $Direction $ArgX', 
        lambda (cmp_, int_, unit_, dir_, arg_): ('.in', ('.extract_text', 
            (dir_, arg_, ('.string', cmp_), int_,('.string', (unit_ if unit_ else 'words')))))), 
            # "between X and Y"
    Rule('$StringToBool', '$Between $ArgXAnd', 
        lambda (btw_, arglist_): 
            ('.in', ('.extract_text', (btw_, arglist_)))), 
    # Indices
    # Rule('$PhraseListOr', '$String', lambda (str_,): ('.str_to_phrases', str_)),
    # Rule('$Phrase', '$ArgX', lambda (arg_,): ('.arg_to_phrase', arg_)),
    # Rule('$Bool', '$Phrase $PhraseToBool', lambda (phr_, func_): ('.call', func_, phr_)),
    #     # "is left of (the word) Y"
    # Rule('$PhraseToBool', '$Direction $Phrase', 
    #     lambda (dir_, phr_): (dir_, ('.gt',), ('.int', 0), phr_)),
    #     # "is two words left of Y"
    # Rule('$PhraseToBool', '$Int ?$Word $Direction $Phrase', 
    #     lambda (int_, word_, dir_, phr_): (dir_, ('.eq',), int_, phr_)),
    #     # "is more than two words left of Y"
    # Rule('$PhraseToBool', '$Compare $Int ?$Word $Direction $Phrase', 
    #     lambda (cmp_, int_, word_, dir_, phr_): (dir_, (cmp_,), int_, phr_)),
    #     # "is within two words of Y"
    # Rule('$PhraseToBool', '$WithIO $Int ?$Word $Phrase', 
    #     lambda (win_, int_, word_, phr_): (win_, int_, phr_)),
    #     # "is between X and Y"
    # # Rule('$PhraseToBool', TBD, lambda sems: TBD,
        
    # Count
            # "the number of (words left of arg 1) is 5"
    Rule('$Int', '$Count $TokenList', sems_in_order),
            # "at least one word is to the left..."
    Rule('$Bool', '$IntToBool $Word $Exists $TokenList', lambda (func_, word_, exist_, list_): 
        ('.call', func_, ('.count', list_))),
            # "at least one noun is to the left..."
    Rule('$Bool', '$IntToBool $POS $Exists $TokenList', lambda sems: 
        ('.call', sems[0], ('.count', ('.filter_by_attr', sems[3], ('.string', 'pos_tags'), sems[1])))),
            # "at least one person is to the left..."
    Rule('$Bool', '$IntToBool $NER $Exists $TokenList', lambda sems: 
        ('.call', sems[0], ('.count', ('.filter_by_attr', sems[3], ('.string', 'ner_tags'), sems[1])))), 
            # "there are not three people to the left..."
    Rule('$Bool', '$Exists $Not $Int $TokenList', lambda sems: ('.call', ('.neq', sems[2]), ('.count', sems[3]))), 
            # "there are three nouns to the left..."
    Rule('$Bool', '$Exists $Int $TokenList', lambda sems: ('.call', ('.eq', sems[1]), ('.count', sems[2]))), 
            # "there are at least two nouns to the left..."
    Rule('$Bool', '$Exists $IntToBool $TokenList', lambda sems: ('.call', sems[1], ('.count', sems[2]))),
    
    
    # Rule('$PhraseList', '$PhraseList $Word', lambda sems: ('.filter_to_alnum', sems[0])),
    # Rule('$PhraseList', '$Word $PhraseList', lambda sems: ('.filter_to_alnum', sems[1])),
    Rule('$PhraseList', '$Word $PhraseList', sems1),
    Rule('$PhraseList', '$POS $PhraseList', lambda sems: ('.filter_by_attr', sems[1], ('.string', 'pos_tags'), sems[0])),
    Rule('$PhraseList', '$NER $PhraseList', lambda sems: ('.filter_by_attr', sems[1], ('.string', 'ner_tags'), sems[0])),
    Rule('$TokenList', '$PhraseList', lambda sems: ('.filter_to_tokens', sems[0])),
    Rule('$StringList', '$PhraseList', lambda sems: ('.extract_text', sems[0])),

    Rule('$String', '$ArgToString $ArgX', lambda (func_, arg_): ('.call', func_, arg_)),
    Rule('$StringListAnd', '$ArgToString $ArgXAnd', lambda (func_, args_): ('.map', func_, args_)),
    Rule('$StringTuple', '$Tuple $StringListAnd', sems_in_order),
    Rule('$TupleToBool', '$In $List', sems_in_order),
    Rule('$Bool', '$StringTuple $TupleToBool', lambda (tup_, func_): ('.call', func_, tup_)),
]

snorkel_rules = lexical_rules + unary_rules + compositional_rules

snorkel_ops = {
    # root
    '.root': lambda x: lambda c: x(c),
    '.label': lambda x, y: lambda c: (1 if x(c)==True else -1) if y(c)==True else 0,
    # primitives
    '.bool': lambda x: lambda c: x,
    '.string': lambda x: lambda c: x,
    '.int': lambda x: lambda c: x,
    # lists
    '.tuple': lambda x: lambda c: tuple(x(c)),
    '.list': lambda *x: lambda c: [z(c) for z in x],
    '.user_list': lambda x: lambda c: c['user_lists'][x(c)],
        # apply a function x to elements in list y
    '.map': lambda x, y: lambda cxy: [x(cxy)(lambda c: yi)(cxy) for yi in y(cxy)],
        # call a 'hungry' evaluated function on one or more arguments
    '.call': lambda *x: lambda c: x[0](c)(x[1])(c), #TODO: extend to more than one argument?
        # apply an element to a list of functions (then call 'any' or 'all' to convert to boolean)
    '.composite_and': lambda x, y: lambda cxy: lambda z: lambda cz: all([x(lambda c: yi)(cxy)(z)(cz)==True for yi in y(cxy)]),
    '.composite_or':  lambda x, y: lambda cxy: lambda z: lambda cz: any([x(lambda c: yi)(cxy)(z)(cz)==True for yi in y(cxy)]),
    # logic
        # NOTE: and/or expect individual inputs, not/all/any/none expect a single iterable of inputs
    '.and': lambda x, y: lambda c: x(c)==True and y(c)==True, 
    '.or': lambda x, y: lambda c: x(c)==True or y(c)==True,
    '.not': lambda x: lambda c: not x(c)==True,
    '.all': lambda x: lambda c: all(xi==True for xi in x(c)),
    '.any': lambda x: lambda c: any(xi==True for xi in x(c)),
    '.none': lambda x: lambda c: not any(xi==True for xi in x(c)),
    # comparisons
    '.eq': lambda x: lambda cx: lambda y: lambda cy: y(cy) == x(cx),
    '.neq': lambda x: lambda cx: lambda y: lambda cy: y(cy) != x(cx),
    '.lt': lambda x: lambda cx: lambda y: lambda cy: y(cy) < x(cx),
    '.leq': lambda x: lambda cx: lambda y: lambda cy: y(cy) <= x(cx),
    '.geq': lambda x: lambda cx: lambda y: lambda cy: y(cy) >= x(cx),
    '.gt': lambda x: lambda cx: lambda y: lambda cy: y(cy) > x(cx),
    # string functions
    '.upper': lambda c: lambda x: lambda cx: x(cx).isupper(),
    '.lower': lambda c: lambda x: lambda cx: x(cx).islower(),
    '.capital': lambda c: lambda x: lambda cx: x(cx)[0].isupper(),
    '.startswith': lambda x: lambda cx: lambda y: lambda cy: y(cy).startswith(x(cx)),
    '.endswith': lambda x: lambda cx: lambda y: lambda cy: y(cy).endswith(x(cx)),
    # lists
    '.in': lambda x: lambda cx: lambda y: lambda cy: y(cy) in x(cx),
    '.contains': lambda x: lambda cx: lambda y: lambda cy: x(cx) in y(cy),
    '.count': lambda x: lambda c: len(x(c)),
    '.sum': lambda x: lambda c: sum(x(c)),
    '.intersection': lambda x, y: lambda c: list(set(x(c)).intersection(y(c))),
    # context
    '.arg': lambda x: lambda c: c['candidate'][x(c) - 1],
        # NOTE: For ease of testing, temporarily allow tuples of strings in place of legitimate candidates
    '.arg_to_string': lambda x: lambda c: x(c) if isinstance(x(c), basestring) else x(c).get_span(),
    '.cid': lambda c: lambda arg: lambda cx: arg(cx).get_attrib_tokens(a='entity_cids')[0], # take the first token's CID
    # sets
    '.left': lambda *x: lambda cx: cx['lf_helpers']['get_left_phrases'](*[xi(cx) for xi in x]),
    '.right': lambda *x: lambda cx: cx['lf_helpers']['get_right_phrases'](*[xi(cx) for xi in x]),
        # '.left': lambda *x: lambda cx: lambda y: lambda cy: cx['lf_helpers']['get_left_phrases'](y(cy), *[xi(cx) for xi in x]),
        # '.right': lambda *x: lambda cx: lambda y: lambda cy: cx['lf_helpers']['get_right_phrases'](y(cy), *[xi(cx) for xi in x]),
        # '.within': lambda *x: lambda c: c['lf_helpers']['get_within_phrases'](*[xi(c) for xi in x]),
    '.between': lambda x: lambda c: c['lf_helpers']['get_between_phrases'](*[xi for xi in x(c)]),
    '.sentence': lambda c: c['lf_helpers']['get_sentence_phrases'](c['candidate'][0]),
    '.extract_text': lambda phrlist: lambda c: [getattr(p, 'text') for p in phrlist(c)],
    # '.extract_field': lambda phrlist, attr: lambda c: [getattr(t, attr(c)) for t in phrlist(c)],
        # TODO: allow multiple-word nouns, etc.
    '.filter_by_attr': lambda phrlist, attr, val: lambda c: [p for p in phrlist(c) if getattr(p, attr(c))[0] == val(c)],
    # '.filter_to_alnum': lambda phrlist: lambda c: [p for p in phrlist(c) if any(letter.isalnum() for letter in getattr(p, 'words'))],
    '.filter_to_tokens': lambda phrlist: lambda c: [p for p in phrlist(c) if len(getattr(p, 'words')) == 1],
    }

def sem_to_str(sem):
    str_ops = {
        '.root': lambda LF: recurse(LF),
        '.label': lambda label, cond: "return {} if {} else 0".format(1 if recurse(label)==True else -1, recurse(cond)),
        '.bool': lambda bool_: bool(bool_),
        '.string': lambda str_: "'{}'".format(str_),
        '.int': lambda int_: int(int_),
        
        '.tuple': lambda list_: "tuple({})".format(recurse(list_)),
        '.list': lambda *elements: "[{}]".format(','.join(recurse(x) for x in elements)),
        '.user_list': lambda name: str(name).upper(),
        '.map': lambda func_, list_: "map({}, {})".format(recurse(func_), recurse(list_)),
        '.call': lambda func_, args_: "call({}, {})".format(recurse(func_), recurse(args_)),

        '.and': lambda x, y: "({} and {})".format(recurse(x), recurse(y)),
        '.or': lambda x, y: "({} or {})".format(recurse(x), recurse(y)),
        '.not': lambda x: "not ({})".format(recurse(x)),
        '.all': lambda x: "all({})".format(recurse(x)),
        '.any': lambda x: "any({})".format(recurse(x)),
        '.none': lambda x: "not any({})".format(recurse(x)),

        '.arg': lambda int_: "arg{}".format(int_),
        '.arg_to_string': lambda arg_: "text({})".format(recurse(arg_)),
        '.cid': lambda arg_: "cid({})".format(recurse(arg_)),

        '.in': lambda rhs: "in {}".format(recurse(rhs)),
        '.contains': lambda rhs: "contains {}".format(recurse(rhs)),

        '.between': lambda list_: "between({})".format(recurse(list_)),
        '.right': lambda *args_: "right({})".format(','.join(recurse(x) for x in args_)),

        '.extract_text': lambda list_: "text({})".format(list_),
    }
    def recurse(sem):
        if isinstance(sem, tuple):
            if sem[0] in str_ops:
                op = str_ops[sem[0]]
                args = [recurse(arg) for arg in sem[1:]]
                return op(*args) if args else op
            else:
                return str(sem)
        else:
            return str(sem)
    return recurse(sem)
        


### DEPRECATED:
    # indices
    # '.arg_to_phrase': lambda arg_: lambda c: c['lf_helpers']['get_phrase_from_span'](arg_(c)),
    # '.str_to_phrases': lambda str_: lambda c: c['lf_helpers']['get_phrases_from_text'](c['candidate'][0].get_parent(), str_(c)),
    # '.left': lambda cmp_, int_, rhs: lambda crhs: lambda lhs: lambda clhs: (
    #     getattr(lhs(clhs),'word_offsets')[0] < getattr(rhs(crhs),'word_offsets')[0] and # left condition
    #     cmp_(lambda c: -(getattr(rhs(crhs),'word_offsets')[0]) + int_(clhs))(crhs)
    #         (lambda c: -(getattr(lhs(clhs),'word_offsets')[0]))(clhs)),
    # '.right': lambda cmp_, int_, rhs: lambda crhs: lambda lhs: lambda clhs: (
    #     getattr(lhs(clhs),'word_offsets')[-1] > getattr(rhs(crhs),'word_offsets')[-1] and # right condition
    #     cmp_(lambda c: getattr(rhs(crhs),'word_offsets')[-1] + int_(clhs))(crhs)
    #     (lambda c: getattr(lhs(clhs),'word_offsets')[-1])(clhs)),
    # '.between':
    # '.within': lambda int_, rhs: lambda crhs: lambda lhs: lambda clhs: (
    #     abs(getattr(lhs(clhs),'word_offsets')[-1] - getattr(rhs(crhs),'word_offsets')[-1]) <= int_(crhs)),
    # '.without': lambda int_, rhs: lambda crhs: lambda lhs: lambda clhs: (
    #     abs(getattr(lhs(clhs),'word_offsets')[-1] - getattr(rhs(crhs),'word_offsets')[-1]) > int_(crhs)),