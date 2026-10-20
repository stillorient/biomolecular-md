# 方法依据与使用边界

整理/链接核对基准日期：2026-10-19。此表承接本次已完成的资料核查；不是系统综述或对论文结果的独立复算。实现文档会更新，生成实际计划时读取与安装版本匹配的文档并保存版本/访问日期。本文所列决策规则为综合设计，不能称为某论文认证的通用工作流。

采用原则：原始研究用于判断适用域；独立基准检验迁移；官方文档核对实现；项目验证确认实际输入与采样。公开 skill 只提供组织形式参考，不作为力场准确性的证据。

| ID | 原始资料/官方来源 | 支持的选择或验证 | 不能据此断言 |
|---|---|---|---|
| E01 | [Reliability and reproducibility checklist for molecular dynamics simulations，2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10014944/)，DOI 10.1038/s42003-023-04653-0 | 目标性质平衡、每条件独立重复与统计、初始构型、实验联系、完整协议共享；至少三次是该清单要求 | 三次或指定时长自动证明收敛；所有任务必须机械采用同一次数 |
| E02 | [Grossfield et al.，Best Practices for Quantification of Uncertainty and Sampling Quality，v1.0](https://livecomsjournal.org/article/5067-best-practices-for-quantification-of-uncertainty-and-sampling-quality-in-molecular-simulations-article-v1-0)，DOI 10.33011/livecoms.1.1.5067，2018 在线/2019 卷期 | 自相关、有效样本、分块误差、采样质量和不确定性 | 误差条覆盖力场所有系统偏差；平稳曲线表示访问了所有相关状态 |
| E03 | [Chodera，2016，A Simple Method for Automated Equilibration Detection](https://pmc.ncbi.nlm.nih.gov/articles/PMC4945107/)，DOI 10.1021/acs.jctc.5b00784 | 针对观测量选择初始剔除段和有效独立样本 | 自动检测能补救未达平衡或发现所有未访问慢状态 |
| E04 | [Cavender et al.，蛋白力场结构基准与实验数据指南，Article v1.0，2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12823150/)，[DOI 10.33011/livecoms.6.1.3871](https://doi.org/10.33011/livecoms.6.1.3871) | 用可反算实验量评估模型；条件、实验/前向模型误差；水也是模型的一部分。使用时核对版本 | 只看与单张晶体结构的 RMSD 即足够验证；任一力场对所有体系最优 |
| E05 | [OpenMM：Running Simulations / Force Fields](https://docs.openmm.org/latest/userguide/application/02_running_sims.html) | 支持的组合、版本化水/离子文件、积分器、约束、输出与 checkpoint/state | 官方能运行意味着在新体系上准确；latest 文档等于本机安装版本 |
| E06 | [OpenMM：Model Building and Editing](https://docs.openmm.org/latest/userguide/application/03_model_building_editing.html) | 加氢/His 处理、溶剂化/离子、额外粒子及组分建模 | 传 pH 后已模拟动态滴定；工具自动选择必然符合真实化学 |
| E07 | [GROMACS：MDP options](https://manual.gromacs.org/current/user-guide/mdp-options.html) | 恒温/恒压、非键与数值参数的实际语义；新模拟不建议 Berendsen barostat | 一个引擎的默认或时间常数可以跨引擎照搬 |
| E08 | [Tian et al.，ff19SB，2019](https://pubs.acs.org/doi/10.1021/acs.jctc.9b00591) | ff19SB 的原始开发/验证、与溶剂共同评估；ff19SB + OPC 可作为有出处的候选 | 所有复合物界面最佳；其他官方支持水组合非法 |
| E09 | [Huang et al.，CHARMM36m](https://www.nature.com/articles/nmeth.4067)，2016 在线/2017 卷期 | 折叠和无序蛋白相关验证及候选模型依据 | 自动覆盖全部修饰肽或准确预测 PPI 结合自由能 |
| E10 | [Robustelli, Piana & Shaw，2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6003505/)，DOI 10.1073/pnas.1800690115 | a99SB-disp、21 个体系及大量实验数据的折叠/无序平衡；精确配套溶剂 | 无序态准确等于 PPI 准确；可以任意替换成别的 TIP4P-D 文件 |
| E11 | [Piana et al.，Development of a Force Field for the Simulation of Single-Chain Proteins and Protein-Protein Complexes，2020](https://pubmed.ncbi.nlm.nih.gov/31914313/)，DOI 10.1021/acs.jctc.9b00251 | 单链与蛋白相互作用应各有验证；本次证据边界为文章记录/摘要，具体协议需读全文 | 本索引已全文复核 DES-Amber 参数，或该模型适用于任意新 PPI |
| E12 | [Assessing the Performance of Peptide Force Fields for Modeling the Solution Structural Ensembles of Cyclic Peptides，2024](https://pubs.acs.org/doi/10.1021/acs.jpcb.4c00157) | 7 组合、12 个五至七残基水中环肽的比较，说明模型新旧不是可靠排名依据。已核对出版页面检索文本；直接全文访问受限 | 将这个集合的排序外推到任意环大小、N-甲基化/D 残基、膜中或蛋白结合态 |
| E14 | [CHARMM-GUI 官方 FAQ](https://www.charmm-gui.org/?doc=faq) | 组件/残基/补丁和格式支持的核实入口；查具体模块/版本 | 构建成功等于参数科学有效，或任何格式转换都保留全部项 |
| E15 | [Constant pH Molecular Dynamics 指南，LiveCoMS 4(1)，2022](https://livecomsjournal.org/index.php/livecoms/article/view/v4i1e1563)，[PMC 全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC9910290/)，DOI 10.33011/livecoms.4.1.1563 | pH 依赖问题的专门方法、状态与实现验证 | 普通固定质子化 MD 已包含恒 pH 效应；任何引擎都同等支持 |
| E16 | [Li & Merz，MCPB.py，2016](https://pubs.acs.org/jcisd8/article/56/4/599/849004/MCPB-py-A-Python-Based-Metal-Center-Parameter)，DOI 10.1021/acs.jcim.5b00674 | 金属中心有键参数化路线的一种工具 | 所有金属均应使用同一模型；固定配位拓扑可无条件描述化学/配位变化 |
| E17 | [MDAnalysis：Centering a trajectory in the box](https://userguide.mdanalysis.org/stable/examples/transformations/center_protein_in_box.html) | make-whole/unwrap、可信键拓扑、居中和 wrap 的区别 | 链质心平移等同分子完整化；旋转坐标可与未旋转盒混用于 PBC |
| E18 | [蛋白–多肽 MM/PBSA/GBSA 基准，2019，53 复合物](https://pubs.rsc.org/en/content/articlehtml/2019/cp/c9cp01674k)，DOI 10.1039/C9CP01674K；[蛋白–蛋白基准，2016，46 复合物](https://pubmed.ncbi.nlm.nih.gov/27444142/)；[Genheden & Ryde 方法综述，2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4487606/) | 分别考虑体系、介电/溶剂化/熵等近似和校准需求；PPI 记录/摘要，综述主要小配体背景 | 三个来源都直接验证任意新蛋白–肽，或端点分数就是 Kd/IC50；旧协议应直接复用 |
| E19 | [PLUMED Masterclass 21.4，Metadynamics](https://www.plumed.org/doc-v2.9/user-doc/html/masterclass-21-4.html) | 增强采样需合适 CV、重加权、误差与收敛；此处是路由/学习依据 | 通用 metadynamics 配方，或者有偏时间就是物理动力学时间；自由能所有方法已被本索引覆盖 |
| E20 | [Knapp, Ospina & Deane，2018，The Importance of Replicas](https://pubs.acs.org/jctcce/article/14/12/6127/752972/Avoiding-False-Positive-Conclusions-in-Molecular)，DOI 10.1021/acs.jctc.8b00391 | 单轨迹假阳性与重复实证；5–10 为研究体系的经验建议 | 任意体系必须固定 5–10 次，或大量短轨迹替代观察慢事件的单次时长 |
| E21 | [PDBFixer 官方手册](https://github.com/openmm/pdbfixer/blob/master/Manual.html) | 缺失残基列表、非标准残基和 heterogen 处理 API 的实际含义 | 修复工具可以替代构建体/化学判断，或所有 HETATM 都应删除 |
| E22 | [OpenMM 8.4.0 Modeller 官方源码](https://github.com/openmm/openmm/blob/8.4.0/wrappers/python/openmm/app/modeller.py) | 已读取加氢、加额外粒子、溶剂化、建膜方法；加氢含最小化，建膜含最小化/积分 | 所有准备 API 都是纯静态；本版行为可不经核对外推到未来版本 |
| E23 | [PDBFixer 1.12 官方源码](https://github.com/openmm/pdbfixer/blob/v1.12/pdbfixer/pdbfixer.py) | 已读 addMissingAtoms/addMissingHydrogens 调用链，修复可包含最小化和短积分 | 禁止运行时也可无条件“先补原子试试” |
| E24 | [Tan et al.，Binding Energy and Free Energy of Calcium Ion to Calmodulin EF-Hands with the Drude Polarizable Force Field](https://pubs.acs.org/doi/10.1021/acsphyschemau.1c00039)，2021 在线/2022 卷期；[PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9718305/) | 相关 EF-hand 的能量/自由能基准提示 C36m 与 Drude-2019 都可能严重高估 Ca²⁺ 结合；本次依据原始来源可检索的方法/结果段落，直接全文访问受限且未复算 | 因有离子参数或短结构稳定即可证明 Ca 结合热力学准确；极化模型自动解决所有偏差；各版本 NBFIX 都已由本论文验证 |

## 使用来源时的记录格式

补充实现依据（2026-10-20 查阅）：**E25** [GROMACS 官方 Force fields 页面](https://manual.gromacs.org/documentation/current/user-guide/force-fields.html)。本次页面标示 2026.4，分别列出 AMBER19SB 配套水说明与 CHARMM 的非键设置，并提示脂质环境需查具体文献。用于说明参数包、引擎和应用环境的数值约定应一起核对，不构成新体系选型或跨版本照抄数值的依据。实际项目继续按安装版本查证。

在实际 A/B 卡记录：决定与参数 → 来源 ID/具体页节 → 来源体系/条件/观测量 → 与当前体系的差异 → 验证及失败动作。读取不到全文就如实标注；不能把摘要推测写成论文的方法细节。遇到关键组分/新方法不在本索引覆盖范围，补查原始论文及实际版本官方文档后再形成可执行计划。

本 skill 参考过 K-Dense 的 [molecular-dynamics 组织框架](https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/molecular-dynamics/SKILL.md)；未复制其运行脚本，也不依赖安装其他 MD skill。原专用流程的启发式链选择、自动删除组分和固定时长不作为此 skill 的默认行为。
