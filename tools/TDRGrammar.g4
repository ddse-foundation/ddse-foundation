/*
 * Copyright (c) 2025 DDSE Foundation
 * Licensed under the MIT License
 */

grammar TDRGrammar;

// Top-level TDR document structure
tdr: frontmatter content EOF;

// YAML frontmatter section
frontmatter: FRONTMATTER_START frontmatterContent FRONTMATTER_END;
frontmatterContent: (yamlLine)*;
yamlLine: YAML_LINE;

// Main content structure
content: (section)*;

// Generic section that can be required or optional
section: sectionHeader sectionContent;
sectionHeader: HASH+ WHITESPACE* sectionTitle NEWLINE;
sectionTitle: (WORD | WHITESPACE | PUNCTUATION)+;
sectionContent: (paragraph | list | codeBlock | table)*;

// Content elements
paragraph: (sentence)+ NEWLINE*;
sentence: (WORD | WHITESPACE | PUNCTUATION | link | emphasis)+ (NEWLINE | EOF);

list: listItem+;
listItem: DASH WHITESPACE+ listContent NEWLINE;
listContent: (WORD | WHITESPACE | PUNCTUATION | link | emphasis)+;

codeBlock: CODE_FENCE_START codeLanguage? NEWLINE codeContent CODE_FENCE_END;
codeLanguage: WORD;
codeContent: (CODE_LINE)*;

table: tableHeader tableRow+;
tableHeader: tableRowContent;
tableRow: tableRowContent;
tableRowContent: PIPE (tableCellContent PIPE)+ NEWLINE;
tableCellContent: (WORD | WHITESPACE | PUNCTUATION | link | emphasis)*;

// Inline elements
link: LINK_START linkText LINK_MIDDLE linkUrl LINK_END;
linkText: (WORD | WHITESPACE | PUNCTUATION)*;
linkUrl: (WORD | PUNCTUATION)+;

emphasis: (BOLD_START (WORD | WHITESPACE | PUNCTUATION)+ BOLD_END) |
          (ITALIC_START (WORD | WHITESPACE | PUNCTUATION)+ ITALIC_END);

// Cross-references (ADR references, etc.)
crossReference: WORD DASH DIGIT+;

// Lexer rules for tokenization
FRONTMATTER_START: '---' NEWLINE;
FRONTMATTER_END: '---' NEWLINE;
YAML_LINE: ~[\r\n]+ NEWLINE;

// Markdown structure tokens
HASH: '#';
DASH: '-' | '*' | '+';
PIPE: '|';

// Code blocks
CODE_FENCE_START: '```' | '~~~';
CODE_FENCE_END: '```' | '~~~';
CODE_LINE: ~[\r\n]* NEWLINE;

// Links
LINK_START: '[';
LINK_MIDDLE: '](';
LINK_END: ')';

// Emphasis
BOLD_START: '**' | '__';
BOLD_END: '**' | '__';
ITALIC_START: '*' | '_';
ITALIC_END: '*' | '_';

// Basic text elements
WORD: [a-zA-Z0-9_]+;
DIGIT: [0-9];
PUNCTUATION: [.,;:!?(){}[\]"'`@#$%^&+=<>/\\];
WHITESPACE: [ \t]+;
NEWLINE: '\r'? '\n';

// Skip whitespace-only lines but preserve structure
WS: [ \t]+ -> skip;

// Comments (for potential future use)
COMMENT: '<!--' .*? '-->' -> skip;
