% This preamble is heavily inspired by Soham Chatterjee's work in
% https://github.com/sohamch08/Eye-Candy-Lecture-Notes-Theme

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{mathnotesrep}[2025/11/16 v1.0]

% tex-fmt: off
% cSpell: disable

%================================
% LOAD BASE CLASS
%================================
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{ctexrep}}
\ProcessOptions\relax
\LoadClass{ctexrep}

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
\RequirePackage[b5paper,margin=1in]{geometry}
\RequirePackage{booktabs}  % better table lines
% Provide support for minipage used in definition environment
\RequirePackage{varwidth}
\RequirePackage[
    backend=biber,      % biber 后端
    style=gb7714-2015,  % 使用 gb7714-2015 样式
    sorting=none,       % 按照引用顺序排序
    autocite=superscript
]{biblatex}
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
\RequirePackage{xeCJKfntef} % for \uline with auto line break in CJK
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
\definecolor{mycorollarycolor}{RGB}{56, 140, 70}
\definecolor{mynotecolor}{RGB}{56, 140, 70}
\definecolor{mytheoremcolor}{RGB}{0,102,204}
\definecolor{mydefinitioncolor}{RGB}{235, 105,12}
\definecolor{myquotecolor}{RGB}{161,143,125}
\definecolor{mycitecolor}{RGB}{0, 102, 204}
\definecolor{myexamplecolor}{RGB}{56, 140, 70}
\definecolor{mydoccolor}{RGB}{0, 73, 145}
\definecolor{myproblemcolor}{RGB}{56, 140, 70}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% TABLE OF CONTENTS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Let's just hope I won't use chapter more than 10 times
\usetikzlibrary{shapes, positioning}
\contentsmargin{0cm}
\titlecontents{chapter}[3.7pc]
{\addvspace{30pt}%
    \begin{tikzpicture}[remember picture, overlay]%
        \draw[fill=mydoccolor!60,draw=mydoccolor!60]
        (-7,-.1) rectangle (-0.6,.5);%
        \pgftext[left,x=-2.5cm,y=0.2cm]{\color{white}\Large\bfseries
        \thecontentslabel};%
\end{tikzpicture}\color{mydoccolor!60}\large\bfseries}%
{}
{}
{\;\titlerule\;\large\bfseries Page \thecontentspage
    \begin{tikzpicture}[remember picture, overlay]
        \draw[fill=mydoccolor!60,draw=mydoccolor!60]
        (2pt,0) rectangle (4,0.1pt);
\end{tikzpicture}}%
\titlecontents{section}[3.7pc]
{\addvspace{2pt}}
{\contentslabel[\textcolor{mydoccolor!80}\thecontentslabel]{2pc}}
{}
{\hfill\small \thecontentspage}
[]
\titlecontents{subsection}[2.7pc]
{\addvspace{-1pt}\small}
{\hspace*{2pc}\contentslabel[\textcolor{mydoccolor!80}\thecontentslabel]{1pc}}
{}
{\hfill\small \thecontentspage}
[]

%{\addvspace{-1pt}\small}
%{}
%{}
%{\ --- \small\thecontentspage}
%[ \textbullet\ ][]

\makeatletter
\renewcommand{\tableofcontents}{%
    \chapter*{%
        \vspace*{-80\p@}%
        \begin{tikzpicture}[remember picture, overlay]%
            \pgftext[right,x=15cm,y=0.2cm]{\color{mydoccolor!60}\Huge\bfseries
            \contentsname};%
            \draw[fill=mydoccolor!60,draw=mydoccolor!60] (13,-.75)
            rectangle (20,1);%
            \clip (13,-.75) rectangle (20,1);
            \pgftext[right,x=15cm,y=0.2cm]{\color{white}\Huge\bfseries
            \contentsname};%
    \end{tikzpicture}}%
\@starttoc{toc}}
\makeatother
%\titleformat{\chapter}[display]
%{\normalfont\Huge\bfseries}{\chaptertitlename\ \thechapter}{20pt}{\Huge}

\newcommand\colorlink[3]{\href{#2}{\color{#1}#3}}
\newcommand\colorurl[2]{{\color{#1}\url{#2}}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% New environments
%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%! Caution: All environments with CAPITALIZED first letter
%! is for internal use only
\tcbuselibrary{theorems,skins,hooks}
%================================
% THEOREM BOX
%================================
% Archive old version
% \makeatletter
% \newtcbtheorem[number within=chapter]{Theorem}{Theorem}{enhanced,
%     breakable,
%     colback=mytheoremcolor!8,
%     colframe=mytheoremcolor,
%     attach boxed title to top left={yshift*=-\tcboxedtitleheight},
%     fonttitle=\bfseries,
%     title={#2},
%     boxed title size=title,
%     boxed title style={%
%         sharp corners,
%         rounded corners=northwest,
%         colback=tcbcolframe,
%         boxrule=0pt,
%     },
%     underlay boxed title={%
%         \path[fill=tcbcolframe] (title.south west)--(title.south east)
%         to[out=0, in=180] ([xshift=5mm]title.east)--
%         (title.center-|frame.east)
%         [rounded corners=\kvtcb@arc] |-
%         (frame.north) -| cycle;
%     },
%     #1
% }{theorem}
% \makeatother
\newtcbtheorem[number within=chapter]{Theorem}{Theorem}
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
\newtcbtheorem[number within=chapter]{Definition}{Definition}
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
% PROBLEM BOX
%================================
\newtcbtheorem[number within=chapter]{Problem}{Problem}
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
% CLAIM BOX
%================================
\newtcbtheorem[number within=chapter]{Claim}{Claim}
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
% COROLLARY BOX
%================================
\newtcbtheorem[number within=chapter]{Corollary}{Corollary}
{%
    enhanced
    ,breakable
    ,colback = mycorollarycolor!10
    ,frame hidden
    ,boxrule = 0sp
    ,borderline west = {2pt}{0pt}{mycorollarycolor}
    ,sharp corners
    ,detach title
    ,before upper = \tcbtitle\par\smallskip
    ,coltitle = mycorollarycolor!85!black
    ,fonttitle = \bfseries\sffamily
    ,description font = \mdseries
    ,separator sign none
    ,segmentation style={solid, mycorollarycolor!85!black}
}
{corollary}

\NewDocumentEnvironment{corollary}{O{} O{}}{%
    \begin{Corollary}{#1}{#2}%
    }{%
    \end{Corollary}%
}

%================================
% NOTE BOX
%================================

\newtcbtheorem[number within=chapter]{Note}{Note}
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
% EXAMPLE BOX
%================================

\newtcbtheorem[number within=chapter]{Example}{Example}
{%
    enhanced
    ,breakable
    ,colback = myexamplecolor!10
    ,frame hidden
    ,boxrule = 0sp
    ,borderline west = {2pt}{0pt}{myexamplecolor}
    ,sharp corners
    ,detach title
    ,before upper = \tcbtitle\par\smallskip
    ,coltitle = myexamplecolor!85!black
    ,fonttitle = \bfseries\sffamily
    ,description font = \mdseries
    ,separator sign none
    ,segmentation style={solid, myexamplecolor!85!black}
}
{example}

\NewDocumentEnvironment{example}{O{} O{}}{%
    \begin{Example}{#1}{#2}%
    }{%
    \end{Example}%
}

%================================
% QUOTE BOX
%================================
\newfontfamily\RefLatinFont{Times New Roman Italic}[]
\newCJKfontfamily\RefCJKFont{STFangsong}[
    AutoFakeSlant = false,
    BoldFont = Heiti SC Medium,
]
\newtcolorbox{refbox}[1][]{%
    enhanced,
    breakable,
    colback = myquotecolor!10,
    frame hidden,
    boxrule = 0sp,
    borderline west = {2pt}{0pt}{myquotecolor},
    sharp corners,
    fontupper = \RefLatinFont\RefCJKFont,
    #1
}
\renewenvironment{quote}{%
\begin{refbox}}{%
\end{refbox}}
% Extra Information
% INFO: Use \mathclap and \substack to create multiline
%================================
% PROOF BOX
%================================
\makeatletter
\renewenvironment{proof}[1][\proofname]{\par
    \pushQED{\qed}%
    \RefCJKFont\topsep6\p@\@plus6\p@\relax
    \trivlist
\item[\hskip\labelsep
        \RefLatinFont\RefCJKFont
    #1\@addpunct{.}]\ignorespaces
}{%
    \popQED\endtrivlist\@endpefalse
}
\makeatother