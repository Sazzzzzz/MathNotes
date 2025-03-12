# `amsthm`

The `amsthm` package is part of the American Mathematical Society's suite of tools for enhancing mathematical typesetting in LaTeX. It provides an easy and flexible way to define theorem-like environments for displaying theorems, definitions, proofs, lemmas, corollaries, and other similar mathematical structures in a consistent and professional manner.

Here’s an overview of how to use the `amsthm` package, along with some key features:

## 1. **Loading the Package**

To use `amsthm`, you need to include it in your preamble:

```latex
\usepackage{amsthm}
```

### 2. **Basic Commands**

The package introduces a few important commands for creating and customizing theorem-like environments.

- **`\newtheorem`**: This command defines new theorem environments.

### Syntax for \newtheorem

```latex
\newtheorem{name}{Printed Name}
```

- `name`: The name of the environment (e.g., `theorem`, `lemma`, `definition`).
- `Printed Name`: The title that will be printed (e.g., "Theorem", "Lemma", "Definition").

### Example for \newtheorem

```latex
\newtheorem{theorem}{Theorem}
\newtheorem{definition}{Definition}
```

This will allow you to use `\begin{theorem} ... \end{theorem}` and `\begin{definition} ... \end{definition}` in the body of your document to define and display theorems and definitions.

### 3. **Numbering Theorems**

By default, theorems are numbered sequentially, but you can customize this behavior to group numbering by sections, chapters, etc.

#### Example 1: Continuous Numbering

```latex
\newtheorem{theorem}{Theorem}  % Numbered 1, 2, 3,...
```

#### Example 2: Numbering by Section

If you want theorems to be numbered within sections (e.g., "Theorem 1.1", "Theorem 1.2", etc.), use the following:

```latex
\newtheorem{theorem}{Theorem}[section]
```

This means that theorem numbering will restart at each section, so theorems in section 1 will be numbered 1.1, 1.2, and so on.

#### Example 3: Shared Numbering Across Environments

If you want different environments to share numbering (e.g., both theorems and lemmas use the same counter), you can define the shared numbering like this:

```latex
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{corollary}[theorem]{Corollary}
```

This way, `theorem`, `lemma`, and `corollary` will share the same numbering sequence.

### 4. **Proofs**

The `amsthm` package also provides a predefined `proof` environment to write proofs with an automatic "Proof" label.

#### Syntax

```latex
\begin{proof}
    ... your proof here ...
\end{proof}
```

The environment automatically appends a Q.E.D. symbol (∎) at the end of the proof, unless you manually suppress or replace it.

#### Example

```latex
\begin{proof}
Let \( x = 2 \). Then \( x + 2 = 4 \), which completes the proof.
\end{proof}
```

You can customize the Q.E.D. symbol with the following command:

```latex
\renewcommand{\qedsymbol}{\blacksquare}
```

### 5. **Customizing Theorem Styles**

`amsthm` allows you to define different styles for various theorem environments, such as italicized or bold titles, and you can create different styles for definitions and remarks (which usually require a non-italic style).

#### Basic Styles

- **Theorem Style**: By default, theorem environments use italic font for their content.
- **Definition Style**: Definitions usually appear in upright (non-italic) text.

You can define these styles using the `\theoremstyle` command:

```latex
\theoremstyle{plain} % The default style for theorems, lemmas, etc.
\newtheorem{theorem}{Theorem}

\theoremstyle{definition} % For definitions, remarks, etc.
\newtheorem{definition}{Definition}

\theoremstyle{remark} % For unnumbered remarks
\newtheorem*{remark}{Remark}
```

### Predefined Styles

1. **`plain`** (default): The title is bold, and the body is italicized. This is used for theorems, lemmas, propositions, corollaries, etc.
2. **`definition`**: The title is bold, and the body is in regular (upright) text. This is suitable for definitions, conditions, and other non-theorem structures.
3. **`remark`**: The title is italicized, and the body is in regular (upright) text. This is typically used for remarks, notes, and unnumbered comments.

### 6. **Unnumbered Theorems**

If you want an unnumbered theorem, you can define it with an asterisk (`*`), like this:

```latex
\newtheorem*{theorem*}{Theorem}
```

This will produce a theorem with the title "Theorem" but without a number.

### Example Document Using `amsthm`

```latex
\documentclass{article}
\usepackage{amsthm}

% Define new theorem environments
\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{corollary}[theorem]{Corollary}

\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}

\theoremstyle{remark}
\newtheorem*{remark}{Remark}

\begin{document}

\section{Sample Theorems}
\begin{theorem}
If \( a \) and \( b \) are real numbers, then \( a + b = b + a \).
\end{theorem}

\begin{proof}
This follows from the commutative property of addition.
\end{proof}

\begin{lemma}
For any integer \( n \), \( n^2 \geq 0 \).
\end{lemma}

\begin{corollary}
If \( n \geq 0 \), then \( n^2 \geq 0 \).
\end{corollary}

\begin{definition}
A number is called positive if it is greater than zero.
\end{definition}

\begin{remark}
This is a simple example to illustrate the use of the `amsthm` package.
\end{remark}

\end{document}
```

### Key Features of `amsthm`

1. **Flexible Theorem Environments**: Define and customize theorem, lemma, corollary, etc.
2. **Proof Environment**: Automatically adds a Q.E.D. symbol at the end of proofs.
3. **Numbering Control**: Supports various numbering schemes (global, by section, or shared numbering).
4. **Styles**: Customizes the appearance of theorem-like environments with different styles (`plain`, `definition`, `remark`).

By using `amsthm`, you gain full control over how your theorems and related mathematical statements are formatted and displayed. Let me know if you need more detailed guidance on any specific feature!
