from __future__ import print_function

from util import CoreNLPHandler
from helpers import lf_helpers

from collections import defaultdict, Iterable
from itertools import product
from six import StringIO
from types import FunctionType

# Grammar ======================================================================

class Grammar(object):
    def __init__(self, rules=[], ops={}, candidate_class=None, annotators=[], 
                 user_lists={}, absorb=True, start_symbol='$ROOT'):
        self.ops = ops
        self.candidate_class = candidate_class
        self.annotators = annotators
        self.user_lists = user_lists
        self.absorb = absorb
        self.categories = set()
        self.lexical_rules = defaultdict(list)
        self.unary_rules = defaultdict(list)
        self.binary_rules = defaultdict(list)
        self.start_symbol = start_symbol
        self.corenlp = CoreNLPHandler()
        for rule in rules:
            self.add_rule(rule)
        for annotator in annotators:
            for rule in annotator.rules:
                self.add_rule(rule)
        if user_lists:
            self.add_rule(Rule('$UserList', ('$UserList', '$Token'), lambda sems: sems[0]))
        print('Created grammar with %d rules' % \
            (len(self.lexical_rules) + len(self.unary_rules) + len(self.binary_rules)))

    def parse_input(self, input):
        """
        Returns the list of parses for the given input which can be derived
        using this grammar.
        """
        input = input.lower()
        tokens = self.corenlp.parse(input)
        # stopwords = ['there','is','are','the','a','an','of','from','away','to','word','words','letter','letters']
        # tokens = [t for i, t in enumerate(tokens) if (
        #     t['word'] not in stopwords or
        #     tokens[max(i-1,0)]['pos'] == "``" or
        #     tokens[min(i+1, len(tokens)-1)]['pos'] == "\'\'"
        #     )
        # ]
        words = [t['word'] for t in tokens]
        chart = defaultdict(list)
        for j in range(1, len(tokens) + 1):
            for i in range(j - 1, -1, -1):
                self.apply_user_lists(chart, tokens, i, j)
                self.apply_annotators(chart, tokens, i, j)
                self.apply_lexical_rules(chart, words, i, j)
                self.apply_binary_rules(chart, i, j)
                self.apply_unary_rules(chart, i, j)
        parses = chart[(0, len(tokens))]
        if self.start_symbol:
            parses = [parse for parse in parses if parse.rule.lhs == self.start_symbol]
        self.chart = chart
        if len(parses) == 0:
            self.print_chart(nested=False, words=words)
            import pdb; pdb.set_trace()
        return parses

    def add_rule(self, rule):
        if rule.contains_optionals():
            self.add_rule_containing_optional(rule)
        elif rule.is_lexical():
            self.lexical_rules[rule.rhs].append(rule)
            if self.absorb:
                self.add_absorption_rule(rule)
        elif rule.is_unary():
            self.unary_rules[rule.rhs].append(rule)
        elif rule.is_binary():
            self.binary_rules[rule.rhs].append(rule)
        elif all([is_cat(rhsi) for rhsi in rule.rhs]):
            self.add_n_ary_rule(rule)
        else:
            # EXERCISE: handle this case.
            raise Exception('RHS mixes terminals and non-terminals: %s' % rule)

    def add_rule_containing_optional(self, rule):
        """
        Handles adding a rule which contains an optional element on the RHS.
        We find the leftmost optional element on the RHS, and then generate
        two variants of the rule: one in which that element is required, and
        one in which it is removed.  We add these variants in place of the
        original rule.  (If there are more optional elements further to the
        right, we'll wind up recursing.)

        For example, if the original rule is:

            Rule('$Z', '$A ?$B ?$C $D')

        then we add these rules instead:

            Rule('$Z', '$A $B ?$C $D')
            Rule('$Z', '$A ?$C $D')
        """
        # Find index of the first optional element on the RHS.
        first = next((idx for idx, elt in enumerate(rule.rhs) if is_optional(elt)), -1)
        assert first >= 0
        assert len(rule.rhs) > 1, 'Entire RHS is optional: %s' % rule
        prefix = rule.rhs[:first]
        suffix = rule.rhs[(first + 1):]
        # First variant: the first optional element gets deoptionalized.
        deoptionalized = (rule.rhs[first][1:],)
        self.add_rule(Rule(rule.lhs, prefix + deoptionalized + suffix, rule.sem))
        # Second variant: the first optional element gets removed.
        # If the semantics is a value, just keep it as is.
        sem = rule.sem
        # But if it's a function, we need to supply a dummy argument for the removed element.
        if isinstance(rule.sem, FunctionType):
            sem = lambda sems: rule.sem(sems[:first] + [None] + sems[first:])
        self.add_rule(Rule(rule.lhs, prefix + suffix, sem))

    def add_absorption_rule(self, rule):
        lhs = rule.lhs
        rhs = (rule.lhs, '$Token')
        new_rule = Rule(lhs, rhs, rule.sem)
        if new_rule not in self.binary_rules[new_rule.rhs]:
            self.binary_rules[new_rule.rhs].append(new_rule)

    def add_n_ary_rule(self, rule):
        """
        Handles adding a rule with three or more non-terminals on the RHS.
        We introduce a new category which covers all elements on the RHS except
        the first, and then generate two variants of the rule: one which
        consumes those elements to produce the new category, and another which
        combines the new category which the first element to produce the
        original LHS category.  We add these variants in place of the
        original rule.  (If the new rules still contain more than two elements
        on the RHS, we'll wind up recursing.)

        For example, if the original rule is:

            Rule('$Z', '$A $B $C $D')

        then we create a new category '$Z_$A' (roughly, "$Z missing $A to the left"),
        and add these rules instead:

            Rule('$Z_$A', '$B $C $D')
            Rule('$Z', '$A $Z_$A')
        """
        def add_category(base_name):
            assert is_cat(base_name)
            name = base_name
            while name in self.categories:
                name = name + '_'
            self.categories.add(name)
            return name
        category = add_category('%s_%s' % (rule.lhs, rule.rhs[0]))
        self.add_rule(Rule(category, rule.rhs[1:], lambda sems: sems))
        self.add_rule(Rule(rule.lhs, (rule.rhs[0], category),
                            lambda sems: rule.apply_semantics([sems[0]] + sems[1])))

    def apply_user_lists(self, chart, tokens, i, j):
        """Add parses to chart cell (i, j) by applying user lists."""
        if self.user_lists:
            words = [t['word'] for t in tokens]
            key = ' '.join(words[i:j])
            if key in self.user_lists:
                lhs = '$UserList'
                rhs = tuple(key.split())
                semantics = ('.user_list', ('.string', key))
                rule = Rule(lhs, rhs, semantics)
                chart[(i, j)].append(Parse(rule, words[i:j]))

    def apply_annotators(self, chart, tokens, i, j):
        """Add parses to chart cell (i, j) by applying annotators."""
        if self.annotators:
            words = [t['word'] for t in tokens]
            for annotator in self.annotators:
                for category, semantics in annotator.annotate(tokens[i:j]):
                    rule = Rule(category, tuple(words[i:j]), semantics)
                    chart[(i, j)].append(Parse(rule, words[i:j]))

    def apply_lexical_rules(self, chart, words, i, j):
        """Add parses to chart cell (i, j) by applying lexical rules."""
        for rule in self.lexical_rules[tuple(words[i:j])]:
            chart[(i, j)].append(Parse(rule, words[i:j]))

    def apply_binary_rules(self, chart, i, j):
        """Add parses to chart cell (i, j) by applying binary rules."""
        for k in range(i + 1, j):
            for parse_1, parse_2 in product(chart[(i, k)], chart[(k, j)]):
                for rule in self.binary_rules[(parse_1.rule.lhs, parse_2.rule.lhs)]:
                    chart[(i, j)].append(Parse(rule, [parse_1, parse_2]))

    def apply_unary_rules(self, chart, i, j):
        """Add parses to chart cell (i, j) by applying unary rules."""
        # Note that the last line of this method can add new parses to chart[(i,
        # j)], the list over which we are iterating.  Because of this, we
        # essentially get unary closure "for free".  (However, if the grammar
        # contains unary cycles, we'll get stuck in a loop, which is one reason for
        # check_capacity().)
        for parse in chart[(i, j)]:
            for rule in self.unary_rules[(parse.rule.lhs,)]:
                chart[(i, j)].append(Parse(rule, [parse]))

    def evaluate(self, parse):
        def recurse(semantics):
            if isinstance(semantics, tuple):
                op = self.ops[semantics[0]]
                args = [recurse(arg) for arg in semantics[1:]]
                return op(*args) if args else op
            else:
                return semantics
        LF = recurse(parse.semantics)
        return lambda candidate: LF({'lf_helpers': lf_helpers(), 'user_lists': self.user_lists, 'candidate': candidate})

    def print_grammar(self):
        def all_rules(rule_index):
            return [rule for rules in list(rule_index.values()) for rule in rules]
        def print_rules_sorted(rules):
            for s in sorted([str(rule) for rule in rules]):
                print('  ' + s)
        print('Lexical rules:')
        print_rules_sorted(all_rules(self.lexical_rules))
        print('Unary rules:')
        print_rules_sorted(all_rules(self.unary_rules))
        print('Binary rules:')
        print_rules_sorted(all_rules(self.binary_rules))

    def print_chart(self, nested=False, words=None):
        """Print the chart.  Useful for debugging."""
        spans = sorted(list(self.chart.keys()), key=(lambda span: span[0]))
        spans = sorted(spans, key=(lambda span: span[1] - span[0]))
        for span in spans:
            if len(self.chart[span]) > 0:
                print('%-12s' % str(span), end=' ')
                if nested:
                    print(self.chart[span][0])
                    for entry in self.chart[span][1:]:
                        print('%-12s' % ' ', entry)
                else:
                    print(' '.join(words[span[0]:span[1]]))
                    for entry in self.chart[span]:
                        print('%-12s' % ' ', entry.rule.lhs)

# Rule =========================================================================

class Rule(object):
    """Represents a CFG rule with a semantic attachment."""

    def __init__(self, lhs, rhs, sem=None):
        self.lhs = lhs
        self.rhs = tuple(rhs.split()) if isinstance(rhs, str) else rhs
        self.sem = sem
        self.validate_rule()

    def __str__(self):
        """Returns a string representation of this Rule."""
        return 'Rule' + str((self.lhs, ' '.join(self.rhs), self.sem))

    def __eq__(self, other):
        return (self.lhs == other.lhs and self.rhs == other.rhs)
    
    def __ne__(self, other):
        return (self.lhs != other.lhs or self.rhs != other.rhs)

    def __hash__(self):
        return hash((self.lhs, self.rhs))

    def apply_semantics(self, sems):
        # Note that this function would not be needed if we required that semantics
        # always be functions, never bare values.  That is, if instead of
        # Rule('$E', 'one', 1) we required Rule('$E', 'one', lambda sems: 1).
        # But that would be cumbersome.
        if isinstance(self.sem, FunctionType):
            return self.sem(sems)
        else:
            return self.sem

    def is_lexical(self):
        """
        Returns true iff the given Rule is a lexical rule, i.e., contains only
        words (terminals) on the RHS.
        """
        return all([not is_cat(rhsi) for rhsi in self.rhs])

    def is_unary(self):
        """
        Returns true iff the given Rule is a unary compositional rule, i.e.,
        contains only a single category (non-terminal) on the RHS.
        """
        return len(self.rhs) == 1 and is_cat(self.rhs[0])

    def is_binary(self):
        """
        Returns true iff the given Rule is a binary compositional rule, i.e.,
        contains exactly two categories (non-terminals) on the RHS.
        """
        return len(self.rhs) == 2 and is_cat(self.rhs[0]) and is_cat(self.rhs[1])

    def validate_rule(self):
        """Returns true iff the given Rule is well-formed."""
        assert is_cat(self.lhs), 'Not a category: %s' % self.lhs
        assert isinstance(self.rhs, tuple), 'Not a tuple: %s' % self.rhs
        for rhs_i in self.rhs:
            assert isinstance(rhs_i, basestring), 'Not a string: %s' % rhs_i

    def contains_optionals(self):
        """Returns true iff the given Rule contains any optional items on the RHS."""
        return any([is_optional(rhsi) for rhsi in self.rhs])

def is_cat(label):
    """
    Returns true iff the given label is a category (non-terminal), i.e., is
    marked with an initial '$'.
    """
    return label.startswith('$')

def is_optional(label):
    """
    Returns true iff the given RHS item is optional, i.e., is marked with an
    initial '?'.
    """
    return label.startswith('?') and len(label) > 1

    
# Parse ========================================================================

class Parse:
    def __init__(self, rule, children):
        self.rule = rule
        self.children = tuple(children[:])
        self.semantics = self.compute_semantics()
        self.function = None
        self.validate_parse()

    def __str__(self):
        child_strings = [str(child) for child in self.children]
        return '(%s %s)' % (self.rule.lhs, ' '.join(child_strings))

    def validate_parse(self):
        assert isinstance(self.rule, Rule), 'Not a Rule: %s' % self.rule
        assert isinstance(self.children, Iterable)
        assert len(self.children) == len(self.rule.rhs)
        for i in range(len(self.rule.rhs)):
            if is_cat(self.rule.rhs[i]):
                assert self.rule.rhs[i] == self.children[i].rule.lhs
            else:
                assert self.rule.rhs[i] == self.children[i]

    def compute_semantics(self):
        if self.rule.is_lexical():
            return self.rule.sem
        else:
            child_semantics = [child.semantics for child in self.children]
            return self.rule.apply_semantics(child_semantics)

    def display(self, indent=0, show_sem=False):
        def indent_string(level):
            return '  ' * level
        def label(parse):
            if show_sem:
                return '(%s %s)' % (parse.rule.lhs, parse.semantics)
            else:
                return parse.rule.lhs
        def to_oneline_string(parse):
            if isinstance(parse, Parse):
                child_strings = [to_oneline_string(child) for child in parse.children]
                return '[%s %s]' % (label(parse), ' '.join(child_strings))
            else:
                return str(parse)
        def helper(parse, level, output):
            line = indent_string(level) + to_oneline_string(parse)
            if len(line) <= 100:
                print(line, file=output)
            elif isinstance(parse, Parse):
                print(indent_string(level) + '[' + label(parse), file=output)
                for child in parse.children:
                    helper(child, level + 1, output)
                # TODO: Put closing parens to end of previous line, not dangling alone.
                print(indent_string(level) + ']', file=output)
            else:
                print(indent_string(level) + parse, file=output)
        output = StringIO()
        helper(self, indent, output)
        return output.getvalue()[:-1]  # trim final newline