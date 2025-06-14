# MathNotes

## True README

这是一个数学笔记仓库！记录了笔者~~重学~~学习数学过程中遇到的有趣数学内容，包括~~试图推倒数学大厦~~、重学线性代数的深度感触`:-o`等等等等～ 笔记全部存储在[`notes`](notes)目录下

同时这也是一个代码库`:-D` 在 [`demos`](demos) 目录下，有一些用`Python`/`Mathematica`编写的分立项目，是笔者在学习数学过程中遇到的有趣问题的代码实现。

目前数学笔记约每周更新一次，包括*实变函数学习笔记*、*线性代数学习笔记*等等，大部分笔记可以在[releases](https://github.com/Sazzzzzz/MathNotes/releases)中直接下载编译完成的PDF版本。*~~（一些见不得人的笔记可以自己编译）~~*

### 行动派指南

**Prequisites**

+ `make`
+ `LaTeX` 环境

本仓库的数学笔记均使用 $\mathrm{\LaTeX}$ 编写，使用`makefile`编译。在确保安装`make`与相应 $\mathrm{\LaTeX}$ 环境后，直接在命令行中输入`make some_notes` (for example `make real_analysis`)即可编译完成，具体的使用方法可用`make help`查看。
编译完成后，PDF文件会在`build`目录下生成。

[`demos`](demos)的配置可见于[`demos/README.md`](demos/README.md)。

> [!NOTE]
>
> 为了加速编译，笔记所有的图片均预先转换为同名PDF文件，存放在每个笔记的`resource` 目录下。若发生编译错误，请务必用`imagemagick`或其他工具将图片转换为PDF格式，VSCode用户可对文件使用存储在`.vscode`目录下的`Convert Image to PDF`任务进行转换。

> [!CAUTION]
> `make github-release` 相关命令是作者方便推送 ~~（图省事加的）~~ 制作的，使用大概率会报错，小概率可能会直接把代码推送到GitHub同名仓库上，请谨慎使用。

### 提建议/意见

笔者数学水平有限，笔记难免缺乏深度，或有错漏之处。欢迎大家在issues中提出各种建议或意见 `:-)` 🙏 🙏

### 许可证

仓库中的所有内容使用[Creative Commons Attribution-NonCommercial 4.0 International License][cc-by-nc]进行许可。

[![CC BY-NC 4.0][cc-by-nc-image]][cc-by-nc]

[cc-by-nc]: http://creativecommons.org/licenses/by-nc/4.0/
[cc-by-nc-image]:https://licensebuttons.net/l/by-nc/4.0/88x31.png

## 一些对笔记的思考

### 笔记真的有用吗？

笔记的概念可以推广为：对事物的记录。包括这篇README在内，整个文档库都是笔记的一种。但这里暂不讨论那些以笔记本身为目的的笔记，而是那些为自己所用的笔记。

1. 对抗遗忘
 对抗遗忘应当是笔记——或者说记录——最为基本的作用。
 最简明扼要的例子就是To-do清单。他最直接的体现了笔记对抗遗忘的作用。
 一个好的笔记，应当能让你在遗忘后通过浏览笔记快速的恢复记忆。
 笔记的这个作用我想是简单的。

2. 加深思考
 我们时常发现，那些工于笔记的人似乎在某一特定的学科上都很强。但笔记作为记忆的载体不能起到加深思考的作用，那笔记与思考的关系究竟是什么呢？
 笔记并不加深思考，但记笔记前、笔记中和笔记后都透露着思考的影子。
   + 笔记前
  在一个自由学习的环境下，当一个人选择记笔记时，他学习的主观能动性就已经被证明了。主观能动性与能力强有相关性。于是记笔记就与能力强就有了相关性。
   + 笔记中
  记笔记是把思考再整理的过程
  记笔记可以看作一种对知识的实践行为。在这个过程中，我们得以遵循某种主线将知识梳理成条理的内容。从某种意义上，我们先前对知识的“感性认识”得以变为全面系统的“理性认识”，最终被我们记下。事实上，当我在记录对笔记的认识时，我对笔记的感性认识也随着记录逐渐变为更加条理的理性认识。这种实践的过程，具有费曼学习法的特征。
   + 笔记后
  我们通过记录笔记后的复习，实现认识的上升。

但事实上我们看到，对于事物的大部分认识，在记录笔记前就已经完成。换句话说，笔记本身与思考和认识毫无关系，但思考和认识无处不在的存在于笔记记录的过程当中。我们之所以认为做笔记的人能力强，是因为笔记与主观能动性的正相关、笔记与条理思考的正相关导致了笔记与实力的正相关。所以你可以看到：著名学习博主考入中专、实现几乎同样目的的费曼学习法如此风靡。笔记不是思考的因，而是思考的果。

### 为什么我们如此狂热于做笔记？

学习是困难的，成果是抽象的，而笔记是具象的。当我们在自由的学习环境下无处标定学习的有效性时，热情有余而方法有限，我们就陷入了一种对笔记的狂热。毕竟，知识写进了笔记里，就是进入了脑海中。从此，我们的大脑得以“解脱“于学习和思考，笔记也就因此成了某种宗教仪式，背上了自我欺骗的骂名。

笔记替代思考正如用消费缓解焦虑一样，是形式替代实质的问题，这也算的上是现代人的通病。

> 我们的坏习惯是把回忆的符号、简化的公式当作本质，最后又当成原因
>
> —— 尼采

### 那为什么还要做笔记？

本仓库的原目的，是记录笔者在学习数学分析中所有课后习题的解答（可见于[`[deprecated]`]([deprecated]/)文件夹）。后来作者发现这样的项目工作量很大，并且已经有成熟的替代品，大多数也是机械的工作，并无意义。

本仓库现今的目的，不是单纯为了记录书上已有的定理或者结论，而是记录那些在学习过程中作者发现的有趣的数学内容，主要作为书上内容的补充。正如简介所言：“Mathematical pebbles gathered during learning” 。本仓库的一大目的，是为了抵抗遗忘。可能另一目的，在于给抽象的数学学习，留一些思考的形式化证明吧。

> Don't just read it; fight it! Ask your own questions, look for your own examples, discover your own proofs. Is the hypothesis necessary? Is the converse true? What happens in the classical special case? What about the degenerate cases? Where does the proof use the hypothesis?
>
> —— Paul Halmos

Copyright © 2025 Caffein3
