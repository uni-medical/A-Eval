# A-Eval 

## 📚 Datasets

| **Dataset** | **Modality** | **# Train** | **# Test** | **# Organs** | **# Organs (Test)** | **Region** |
|:-----------:|:------------:|:-----------:|:----------:|:------------:|:------------------:|:----------:|
| FLARE22     | CT           | 50 labeled <br> 2000 unlabeled | 50 | 13 | 10 | North America <br> Europe |
| AMOS CT     | CT           | 200         | 40         | 15          | 10                 | Asia       |
| WORD        | CT           | 100         | 30         | 16          | 10                 | Asia       |
| TotalSegmentator v2 | CT   | 1082        | 89         | 117         | 10                 | Europe     |
| BTCV        | CT           | -           | 30         | 13          | 10                 | North America |
| AMOS MR     | MR           | 40          | 20         | 15          | 10                 | Asia       |
| TotalSegmentator MR | MR   | 268         | 30         | 56          | 10                 | Europe     |
| **A-Eval Totals** | **CT & MR** | **1432 labeled CT** <br> **2000 unlabeled CT** <br> **308 MR** | **239 CT** <br> **50 MR** | **10** | **10** | **North America** <br> **Europe** <br> **Asia** |

To ensure a meaningful and fair comparison across datasets, we evaluate the models' performance based on a set of ten organ classes shared by all datasets. We unify these labels using an overlapped label system. The corresponding code for label systems and label conversion can be found in the repository: [`label_systems.py`](Evaluation/label_systems.py) and [`convert_label_2_overlap_label.py`](Evaluation/convert_label_2_overlap_label.py).

| Organ Class            | **FLARE22** | **AMOS CT** | **WORD*** | **TotalSegmentator v2** | **AMOS MR** | **TotalSegmentator MR** | **A-Eval** |
|:-----------------------|:-----------:|:-----------:|:---------:|:----------------------:|:-----------:|:----------------------:|:----------:|
| Liver                  |      ✓      |      ✓      |     ✓     |           ✓           |      ✓      |           ✓           |     ✓      |
| Kidney Right           |      ✓      |      ✓      |     ✓     |           ✓           |      ✓      |           ✓           |     ✓      |
| Kidney Left            |      ✓      |      ✓      |     ✓     |           ✓           |      ✓      |           ✓           |     ✓      |
| Spleen                 |      ✓      |      ✓      |     ✓     |           ✓           |      ✓      |           ✓           |     ✓      |
| Pancreas               |      ✓      |      ✓      |     ✓     |           ✓           |      ✓      |           ✓           |     ✓      |
| Aorta                  |      ✓      |      ✓      |     ✗     |           ✓           |      ✓      |           ✓           |     ✗      |
| Inferior Vena Cava     |      ✓      |      ✓      |     ✗     |           ✓           |      ✓      |           ✓           |     ✗      |
| Adrenal Gland Right    |      ✓      |      ✓      |     ✓     |           ✓           |      ✓      |           ✓           |     ✓      |
| Adrenal Gland Left     |      ✓      |      ✓      |     ✓     |           ✓           |      ✓      |           ✓           |     ✓      |
| Gallbladder            |      ✓      |      ✓      |     ✓     |           ✓           |      ✓      |           ✓           |     ✓      |
| Esophagus              |      ✓      |      ✓      |     ✓     |           ✓           |      ✓      |           ✓           |     ✓      |
| Stomach                |      ✓      |      ✓      |     ✓     |           ✓           |      ✓      |           ✓           |     ✓      |
| Duodenum               |      ✓      |      ✓      |     ✓     |           ✓           |      ✓      |           ✓           |     ✗      |

*Note: The WORD dataset has been post-processed to distinguish between left and right adrenal glands.

## 🎫 License
This project is released under the [Apache 2.0 license](LICENSE). 

## 🙏 Acknowledgement
- Special thanks go to the creators and maintainers of the public datasets that made our research possible:
  - [FLARE22](https://flare22.grand-challenge.org/)
  - [AMOS](https://amos22.grand-challenge.org/)
  - [WORD](https://github.com/HiLab-git/WORD)
  - [TotalSegmentator](https://github.com/wasserth/TotalSegmentator)
  - [BTCV](https://www.synapse.org/#!Synapse:syn3193805/wiki/217752)
- Thanks to the SOTA framework of: [nnUNet](https://github.com/MIC-DKFZ/nnUNet)

## 👋 Hiring & Global Collaboration
- **Hiring:** We are hiring researchers, engineers, and interns in General Vision Group, Shanghai AI Lab. If you are interested in Medical Foundation Models and General Medical AI, including designing benchmark datasets, general models, evaluation systems, and efficient tools, please contact us.
- **Global Collaboration:** We're on a mission to redefine medical research, aiming for a more universally adaptable model. Our passionate team is delving into foundational healthcare models, promoting the development of the medical community. Collaborate with us to increase competitiveness, reduce risk, and expand markets.
- **Contact:** Junjun He(hejunjun@pjlab.org.cn), Jin Ye(yejin@pjlab.org.cn), and Tianbin Li (litianbin@pjlab.org.cn).