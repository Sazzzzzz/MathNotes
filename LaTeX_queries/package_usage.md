# Package Usage

1. `titlesec`

    Purpose: Customizes the appearance of sectioning commands like `\chapter`, `\section`, etc.

    Common Usage: Allows you to change the format, font size, spacing, and indentation of section titles.

    Example:

   ```tex
   \titleformat{\section}{\Large\bfseries}{\thesection}{1em}{}
   \titlespacing*{\section}{0pt}{2ex}{1ex}
   ```

   The above example changes the section font to \Large and \bfseries (bold), and adjusts the spacing before and after sections.
2. `tcolorbox`

   Purpose: Creates highly customizable colored boxes. The option `[many]` enables many additional features, including breaking boxes across pages.

   Common Usage: Often used for highlighting important text, creating theorem/proof boxes, or problems in exercises.

   Example:

    ```tex
    \usepackage[many]{tcolorbox}
    \tcbset{colback=blue!5!white, colframe=blue!75!black, fonttitle=\bfseries}
    \begin{tcolorbox}[title=Important]
    This is an important note.
    \end{tcolorbox}
   ```

3. `amsfonts`

   Purpose: Provides access to additional mathematical fonts from the AMS (American Mathematical Society). These fonts include symbols like `\mathbb{R}` for the set of real numbers.

   Common Usage: Used for set notations, special symbols, and script-style fonts.

   Example:

    ```tex
    \mathbb{R}, \mathbb{Z}, \mathfrak{g}
    ```

4. `amsmath`

   Purpose: A powerful package for improving mathematical typesetting. It enhances the handling of equations, aligning multiple equations, and many advanced math structures.

   Common Usage: Typesetting complex equations and aligning them properly in documents.

   Example:

    ```tex
    \begin{align}
    x^2 + y^2 &= z^2 \\
    a + b &= c
    \end{align}
    ```

5. `amsthm`

   Purpose: Facilitates the creation and formatting of theorem-like environments such as theorem, lemma, corollary, proof, etc.

   Common Usage: Used to define and customize theorems, definitions, and other environments for mathematical reasoning.

   Example:

    ```tex
    \newtheorem{theorem}{Theorem}
    \begin{theorem}
    Every prime number greater than 2 is odd.
    \end{theorem}
    ```

6. `amssymb`

   Purpose: Provides access to additional mathematical symbols not included in the base LaTeX installation or amsmath. It adds symbols for logic, set theory, and others.

   Common Usage: Provides symbols like `\triangleq` (defined as), `\leqslant`, and `\geqslant`.

   Example:

   ```tex
   \leqslant, \geqslant, \nRightarrow
   ```

7. `dsfont`

   Purpose: Adds the ability to typeset double-struck characters, particularly useful for sets and indicators. It offers an alternative to the `\mathbb{}` provided by amsfonts.

   Common Usage: Often used to define the indicator function (e.g., `\mathds{1}`) or to represent common sets like `\mathds{R}` for real numbers.

   Example:

    ```tex
    \mathds{R}, \mathds{1}
    ```

8. `esint`

   Purpose: Extends the selection of integrals beyond the standard set provided by LaTeX, including multiple integrals and contour integrals.

   Common Usage: Allows for special integral signs like \oiint (closed surface integral) and \varointctrclockwise.

   Example:

    ```tex
    \oiint, \varointclockwise
    ```

9. `enumerate`

   Purpose: Enhances the standard enumerate environment for creating numbered lists.

   Common Usage: Allows custom labels for enumerated lists.

   Example:

    ```tex
    \begin{enumerate}
        \item First item
        \item Second item
    \end{enumerate}
    ```

10. `enumitem`

    Purpose: Provides more control over list environments like itemize and enumerate. The shortlabels option makes customizing labels in enumerate easier.

    Common Usage: Allows setting custom spacing, labeling, and more for lists.

    Example:

    ```tex
    \begin{enumerate}[label=(\roman*)]
        \item First item
        \item Second item
    \end{enumerate}
    ```

11. `framed`

    Purpose: Allows you to put frames around blocks of text or other content. It’s useful for highlighting key sections or examples.

    Common Usage: Wraps content in a frame to make it stand out.

    Example:

    ```tex
    \begin{framed}
    This is some framed text.
    \end{framed}
    ```

12. `csquotes`

    Purpose: Simplifies the handling of quotation marks in LaTeX documents. It automatically adjusts quotes to the language settings and typography rules, and supports nested quotes.

    Common Usage: Typesets quotes correctly, especially in multi-language documents.

    Example:

    ```tex
    \enquote{This is a quotation.}
    ```
