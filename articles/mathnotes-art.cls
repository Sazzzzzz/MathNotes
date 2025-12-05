% This preamble is heavily inspired by Soham Chatterjee's work in
% https://github.com/sohamch08/Eye-Candy-Lecture-Notes-Theme

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{mathnotesart}[2025/11/16 v1.0]

% tex-fmt: off
% cSpell: disable

%================================
% LOAD BASE CLASS
%================================
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{ctexart}}
\ProcessOptions\relax
\LoadClass{ctexart}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% PACKAGE IMPORTS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage{amsthm}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
% For augmented matrices, from https://tex.stackexchange.com/questions/2233/whats-the-best-way-make-an-augmented-coefficient-matrix
\makeatletter
\renewcommand*\env@matrix[1][*\c@MaxMatrixCols c]{%
    \hskip -\arraycolsep
    \let\@ifnextchar\new@ifnextchar
    \array{#1}}
\makeatother
\RequirePackage[a4paper,scale=0.8]{geometry}
\RequirePackage{booktabs}  % better table lines
% Provide support for minipage used in definition environment
\RequirePackage{varwidth}
\RequirePackage[style=numeric-comp,autocite=superscript]{biblatex}
\RequirePackage{array} % enhanced table features
% Underline and strikethrough
\RequirePackage[normalem]{ulem}
\RequirePackage[dvipsnames]{xcolor}
\RequirePackage[most,many,breakable]{tcolorbox}
\RequirePackage{extarrows}
% better \d symbol
\RequirePackage{derivative}
\RequirePackage{tikz-cd}
% Make sure all math formulas are displayed in displaystyle
\RequirePackage{breqn}
% Some may argue that the use of displaystyle in inline formulas may
% break line spacing and make the document look ugly. However, I
% prefer to follow the choice of the textbook setting
\everymath{\displaystyle}
% For \mathscr
\RequirePackage{mathrsfs}
\RequirePackage{graphicx}
% Title and ToC format
\RequirePackage{titletoc,titlesec}
\RequirePackage{float}
\RequirePackage{tikz}
% For bold math symbols
\RequirePackage{bm}
\RequirePackage{mathtools} % For \coloneqq
\RequirePackage{hyperref}
\hypersetup{%
 colorlinks=true, linkcolor=mydoccolor!80, urlcolor=mydoccolor!80,
 citecolor=mycitecolor!80!black,
 bookmarksnumbered=true,
 bookmarksopen=true
}
\RequirePackage{cleveref}
\RequirePackage{titling}
% Use verb inside other environments
\RequirePackage{fancyvrb}
\VerbatimFootnotes
\SaveVerb{smile}|:-)|
\SaveVerb{laugh}|:-D|
\SaveVerb{wink}|;-)|
\SaveVerb{sad}|:-(|
\SaveVerb{angry}|:-@|
\SaveVerb{confused}|:-S|
\SaveVerb{cool}|B-)|
\SaveVerb{cry}|:'-|
\SaveVerb{kiss}|:-*|
\SaveVerb{surprised}|:-o|
\SaveVerb{grin}|:-]|
\SaveVerb{naughty}|:P|
\SaveVerb{relaxed}|:-|%
\SaveVerb{froze}!:|!% % use ! as delimiter to avoid conflict with |
% For cancel line
\RequirePackage{cancel}
% For code highlighting
\RequirePackage{listings}
\newfontfamily{\Cascadia}{Cascadia Code}
\lstset{language=Mathematica}
\lstset{basicstyle={\Cascadia\footnotesize},
    numbers=left,
    numberstyle=\tiny\color{gray},
    numbersep=5pt,
    breaklines=true,
    captionpos={t},
    frame={lines},
    rulecolor=\color{black},
    framerule=0.5pt,
    columns=flexible,
    tabsize=4
}

%================================
% PAGE SETUP
%================================

\renewcommand{\thesection}{\textbf{\chinese{section}}、\hspace{-1em}}
\renewcommand{\thesubsection}{\arabic{subsection}.\hspace{-0.3em}}
\renewcommand{\thesubsubsection}{\arabic{subsubsection}}
\catcode`\。=\active\newcommand{。}{．}
\ctexset{section={format={\Large\raggedright\bfseries}}}

%================================
% MATH COMMANDS
%================================
\AtBeginDocument{%
\renewcommand\Re{\operatorname{Re}}
\renewcommand\Im{\operatorname{Im}}
}
\renewcommand{\i}{\mathrm{i}}
\newcommand{\e}{\mathrm{e}}
\renewcommand{\d}{\odif}

\newcommand{\R}{\mathbb{R}} % Real
\newcommand{\C}{\mathbb{C}} % Complex
\newcommand{\Z}{\mathbb{Z}} % Integer, from Zahlen, by David Hilbert
\newcommand{\Q}{\mathbb{Q}} % Rational, from Quotient
\newcommand{\N}{\mathbb{N}} % Natural, from Naturals

\newcommand{\abs}[1]{\left|#1\right|} % Absolute value

\newcommand{\placeholder}[1]{\mathrel{\phantom{#1}}} % Placeholder

\crefname{equation}{式}{式}
\Crefname{equation}{式}{式}
\crefname{theorem}{定理}{定理}
\Crefname{theorem}{定理}{定理}
\crefname{definition}{定义}{定义}
\Crefname{definition}{定义}{定义}
\crefname{problem}{问题}{问题}
\Crefname{problem}{问题}{问题}
\crefname{claim}{断言}{断言}
\Crefname{claim}{断言}{断言}
\crefname{note}{注}{注}
\Crefname{note}{注}{注}

%================================
% DOCUMENT SETUP
%================================

\newcommand\hl{\bgroup\markoverwith{\textcolor{yellow}{\rule[-.5ex]{2pt}{2.5ex}}}\ULon}

\newfontfamily\DancingScript{Dancing Script OT}
\newcommand{\Caffein}{\DancingScript{Caffein3}}
% Predefine title, author and date
\author{\Large \Caffein}
\date{}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% COLORS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\definecolor{myclaimcolor}{RGB}{56, 140, 70}
\definecolor{mynotecolor}{RGB}{56, 140, 70}
\definecolor{mytheoremcolor}{RGB}{0,102,204}
\definecolor{mydefinitioncolor}{RGB}{235, 105,12}
\definecolor{myquotecolor}{RGB}{161,143,125}
\definecolor{mycitecolor}{RGB}{0, 102, 204}
\definecolor{myexamplecolor}{RGB}{56, 140, 70}
\definecolor{mydoccolor}{RGB}{0, 73, 145}
\definecolor{myproblemcolor}{RGB}{56, 140, 70}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% New environments
%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%! Caution: All environments with CAPITALIZED first letter
%! is for internal use only
\tcbuselibrary{theorems,skins,hooks}
%================================
% THEOREM BOX
%================================
\newtcbtheorem{Theorem}{Theorem}
{%
    enhanced,
    breakable,
    colback = mytheoremcolor!10,
    frame hidden,
    boxrule = 0sp,
    borderline west = {2pt}{0pt}{mytheoremcolor},
    sharp corners,
    detach title,
    before upper = \tcbtitle\par\smallskip,
    coltitle = mytheoremcolor!85!black,
    fonttitle = \bfseries\sffamily,
    description font = \mdseries,
    separator sign none,
    segmentation style={solid, mytheoremcolor!85!black},
}
{theorem}

\NewDocumentEnvironment{theorem}{O{} O{}}{%
    \begin{Theorem}{#1}{#2}%
    }{%
    \end{Theorem}%
}

%================================
% DEFINITION BOX
%================================
\newtcbtheorem{Definition}{Definition}
{%
    enhanced,
    breakable,
    colback = mydefinitioncolor!10,
    frame hidden,
    boxrule = 0sp,
    borderline west = {2pt}{0pt}{mydefinitioncolor},
    sharp corners,
    detach title,
    before upper = \tcbtitle\par\smallskip,
    coltitle = mydefinitioncolor!85!black,
    fonttitle = \bfseries\sffamily,
    description font = \mdseries,
    separator sign none,
    segmentation style={solid, mydefinitioncolor!85!black},
}
{definition}

\NewDocumentEnvironment{definition}{O{} O{}}{%
    \begin{Definition}{#1}{#2}%
    }{%
    \end{Definition}%
}

%================================
% EXAMPLE BOX
%================================
\newtcbtheorem{Example}{Example}
{%
    enhanced,
    breakable,
    colback = myexamplecolor!10,
    frame hidden,
    boxrule = 0sp,
    borderline west = {2pt}{0pt}{myexamplecolor},
    sharp corners,
    detach title,
    before upper = \tcbtitle\par\smallskip,
    coltitle = myexamplecolor!85!black,
    fonttitle = \bfseries\sffamily,
    description font = \mdseries,
    separator sign none,
    segmentation style={solid, myexamplecolor!85!black},
}
{example}

\NewDocumentEnvironment{example}{O{} O{}}{%
    \begin{Example}{#1}{#2}%
    }{%
    \end{Example}%
}

%================================
% CLAIM BOX
%================================
\newtcbtheorem{Claim}{Claim}
{%
    enhanced
    ,breakable
    ,colback = myclaimcolor!10
    ,frame hidden
    ,boxrule = 0sp
    ,borderline west = {2pt}{0pt}{myclaimcolor}
    ,sharp corners
    ,detach title
    ,before upper = \tcbtitle\par\smallskip
    ,coltitle = myclaimcolor!85!black
    ,fonttitle = \bfseries\sffamily
    ,description font = \mdseries
    ,separator sign none
    ,segmentation style={solid, myclaimcolor!85!black}
}
{claim}

\NewDocumentEnvironment{claim}{O{} O{}}{%
    \begin{Claim}{#1}{#2}%
    }{%
    \end{Claim}%
}

%================================
% PROBLEM BOX
%================================
\newtcbtheorem{Problem}{Problem}
{%
    enhanced,
    breakable,
    colback = myproblemcolor!10,
    frame hidden,
    boxrule = 0sp,
    borderline west = {2pt}{0pt}{myproblemcolor},
    sharp corners,
    detach title,
    before upper = \tcbtitle\par\smallskip,
    coltitle = myproblemcolor!85!black,
    fonttitle = \bfseries\sffamily,
    description font = \mdseries,
    separator sign none,
    segmentation style={solid, myproblemcolor!85!black},
}
{problem}

\NewDocumentEnvironment{problem}{O{} O{}}{%
    \begin{Problem}{#1}{#2}%
    }{%
    \end{Problem}%
}

%================================
% NOTE BOX
%================================

\newtcbtheorem{Note}{Note}
{%
    enhanced
    ,breakable
    ,colback = mynotecolor!10
    ,frame hidden
    ,boxrule = 0sp
    ,borderline west = {2pt}{0pt}{mynotecolor}
    ,sharp corners
    ,detach title
    ,before upper = \tcbtitle\par\smallskip
    ,coltitle = mynotecolor!85!black
    ,fonttitle = \bfseries\sffamily
    ,description font = \mdseries
    ,separator sign none
    ,segmentation style={solid, mynotecolor!85!black}
}
{note}

\NewDocumentEnvironment{note}{O{} O{}}{%
    \begin{Note}{#1}{#2}%
    }{%
    \end{Note}%
}
%================================
% QUOTE BOX
%================================
\newtcolorbox{refbox}[1][]{%
    enhanced,
    breakable,
    colback = myquotecolor!10,
    frame hidden,
    boxrule = 0sp,
    borderline west = {2pt}{0pt}{myquotecolor},
    sharp corners,
    fontupper = \ttfamily,
    #1
}
\renewenvironment{quote}{%
\begin{refbox}}{%
\end{refbox}}

\endinput
