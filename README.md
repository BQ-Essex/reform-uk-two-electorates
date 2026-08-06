# One Coalition, Two Electorates: Cross-Pressure in the Reform UK Vote

**Bradley Quinlan**, 2026 · MA336 *Artificial Intelligence and Machine Learning with Applications*, University of Essex

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Jupyter](https://img.shields.io/badge/Jupyter-notebook-orange)
![scikit-learn](https://img.shields.io/badge/scikit--learn-PCA%20·%20K--means%20·%20trees-F7931E)
![License: MIT](https://img.shields.io/badge/Code%20License-MIT-green)
[![Build report](https://github.com/BQ-Essex/reform-uk-two-electorates/actions/workflows/build-report.yml/badge.svg)](https://github.com/BQ-Essex/reform-uk-two-electorates/actions/workflows/build-report.yml)

A multi-method, multi-dataset machine-learning study of whether Reform UK's 2024
electorate is a single bloc or several.

> **Headline finding:** clustered on political attitudes alone, Reform's 2024 voters
> split almost in half—**55%** in a conventional right-authoritarian group and
> **41%** in an **authoritarian-left** group that is pro-redistribution, left-leaning,
> and markedly the least credentialled of the three, sitting inside a party that campaigned on
> tax cuts it costed at **~£90bn a year**. Projected onto 2014 UKIP identifiers, the
> "left-behind" cluster is *larger* still (59%), so the pattern predates Reform by a decade.

## What's here

| Path | What it is |
|------|-----------|
| [`notebook/`](notebook/) | The full analysis notebook—code, narrative and figures inline. This is the primary artefact. |
| [`report/report.html`](report/) | The complete write-up rendered for reading—prose, figures and tables, with the code kept in the notebook. |
| [`report/SUMMARY.html`](report/SUMMARY.html) | The short summary, styled to match the report. |
| [`report/SUMMARY.md`](report/SUMMARY.md) | A short, code-free reader's version—prose, figures and headline numbers. |
| [`figures/`](figures/) | The eleven figures exported from the analysis. |
| [`data/`](data/) | The two open datasets, plus a README on obtaining the restricted survey data. |
| [`fonts/`](fonts/) | Lora and Lato TTFs, embedded by `build_report.py` into `report.html`. |

## The question

Cross-pressure theory describes a base that is socially hardline yet economically left as
"left behind" (Ford & Goodwin)—a thesis that is contested (Evans & Mellon) and since
reframed around identity and education (*Brexitland*). This project tests, with machine
learning rather than assertion, whether that internal tension actually shows up *inside*
Reform's own voters, whether it is robust to how it is measured, and whether it is long-standing.

## Method, in brief

Rather than trust one model, several are made to cross-examine each other on the 2024
British Social Attitudes Survey—and where they disagree, the disagreement is diagnosed
rather than hidden:

- **PCA** finds the attitudinal axes (PC1 = the familiar left–right fusion; PC2 = the
  authoritarian-left vs libertarian-right signature the project is built around).
- **K-means** clustering, with a transparent judgement to use *k*=3 rather than the
  silhouette-optimal *k*=2 (which is itself the two-cluster story the title states).
- **Two autoencoders**—a `tanh`-bottleneck network and a from-scratch, framework-free
  linear-bottleneck one—used as an honest probe of nonlinearity. Together they show the
  linear subspace is adequate for *reconstruction* but that the fine partition is
  *embedding-sensitive*, which is where the analysis's real uncertainty turns out to sit.
- **Hierarchical (Ward) clustering** agrees substantially with K-means (ARI 0.75), with the
  only disagreement at the soft boundary between the two Reform clusters.
- **Robustness checks**—dropping the weakest variable, clustering on the full 5-D space,
  a third component, and a bootstrap—leave the split essentially unchanged (Cluster-1
  membership is stable across resamples at probability 0.98).
- A **supervised decision tree** independently leans on the same dominant attitude and
  struggles to classify the cross-pressured cluster, exactly as such a group should.
- A **longitudinal projection** onto 2014 UKIP identifiers, with a difference-in-differences
  test showing the coalition *broadened by adding* conventional-right voters rather than
  shedding its left-behind core.
- A **direct test of the *Brexitland* education thesis**: the cross-pressured cluster is the
  least-credentialled of the three, and the gap holds net of class and income—education acting
  as more than an economic proxy, as the successor thesis predicts.
- A **precise name for the cross-pressure**: the second cluster is pro-redistribution *and*
  welfare-sceptical *and* anti-immigration (on the split-ballot items—small n—around four in five
  rate immigration bad for the economy). Redistribution to an implied in-group, held alongside
  hostility to an out-group's claims on the same welfare state, is what the literature calls
  **welfare chauvinism** (Andersen & Bjørklund, 1990; Careja & Harris, 2022)—a sharper and less
  paradoxical description than "a left-wing electorate inside a right-wing party."

## Selected figures

![PCA biplot of the attitudinal feature space](figures/fig03_pca-biplot.png)

![K-means k=3 clusters on the PCA components](figures/fig05_kmeans-clusters-k3-scatter.png)

## Scope & caveats

The claims here are deliberately **descriptive**, not predictive. The Reform subsample is
modest, the clustering is unweighted (though reweighting to BSA's published weights leaves the split essentially unchanged, at 52/44/4), and some subgroups are small—so these are structural
patterns in attitudes, not turnout forecasts. The "welfare-reliant" character of the second
cluster is a *compositional* fact, and a deliberately bounded one: `Anybn3` counts the state pension
and other age-related transfers, so the headline 53% largely tracks age, the two Reform clusters are
indistinguishable above 65, and the working-age gap (38% against 26%) is suggestive at p = 0.079
rather than established (Section 7a). It is not a claim about welfare *attitudes* either—on
the welfare-attitudes scale itself, the second cluster is about as sceptical of claimants as the
conventional right-authoritarian cluster is. That combination (pro-redistribution, welfare-sceptical,
anti-immigration) is what the report names *welfare chauvinism* rather than describing the cluster
as generically left-wing.

The 2014→2024 comparison is two independent survey cross-sections, not a panel, so it can show
that the authoritarian-left profile is durable and that the coalition's *composition* shifted
(a difference-in-differences finds it added a conventional-right layer rather than shedding its
left-behind core)—it cannot show that any individual voter changed their mind. Confirming
conversion versus composition at the individual level would need panel data (e.g. the British
Election Study), which is beyond what a repeated cross-section can settle.

The geographic-triangulation section (aggregate regional cluster shares against regional vote
share and deprivation) is a supplementary cross-check, not load-bearing evidence: it compares
two different kinds of electorate at the aggregate level, so it carries the usual ecological-inference
caveat and is not asked to substitute for the individual-level clustering the rest of the project
relies on.

The confidence in the central finding comes not from any single model but from its recurrence
across linear and non-linear, supervised and unsupervised methods, and across a decade of data.

## Reproducing the analysis

```bash
pip install -r requirements.txt
# obtain the restricted BSA files (see data/README.md) and place them in data/
jupyter lab notebook/MA336_Project_Notebook.ipynb   # run from the repo root
```

The two open datasets are already included, so the geographic-triangulation section runs
out of the box; the core clustering additionally requires the two BSA files.

Some IDEs (Positron, VS Code) set a notebook's working directory to the notebook's own
folder rather than wherever you launched from, regardless of the `# run from the repo
root` command above—if a `data/...` path 404s, that's why. Either point your IDE's
notebook working-directory setting at the project root, or place a second copy of
`data/` inside `notebook/` as a workaround.

`report/report.html` is generated from the notebook by `build_report.py`
(`pip install markdown`), so editing the notebook and re-running the script keeps the
two in sync. It embeds Lora and Lato as base64 web fonts, reading the TTFs bundled in
[`fonts/`](fonts/) (SIL Open Font License—see [`fonts/README.md`](fonts/README.md)),
so this runs unmodified on any platform. The notebook registers the same bundled TTFs
for its own figures, so a top-to-bottom run reproduces the report's typography rather
than falling back to a default face.

It does not regenerate `SUMMARY.html`, which is maintained by hand and embeds its own
copy of each figure. Changing a figure therefore means updating `SUMMARY.html`
too—`build_report.py` will not do it for you, and CI only diffs `report.html`.

The two print PDFs are then built from `report.html` and `SUMMARY.html` as they stand
by `build_pdf.py` (`pip install weasyprint`). WeasyPrint's Python package alone isn't
enough—it also needs Pango, a native library, installed at the OS level: on macOS,
`brew install pango`; see [WeasyPrint's install docs](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation)
for Linux/Windows. This step is only needed to rebuild the PDFs from source—the
built PDFs are already committed in `report/`, so reading the report doesn't require
it. `print.css` is applied only at render time—full-bleed canvas tint, A4 page
size, a running header/footer, and forced wrapping on wide code/data blocks and
tables so nothing runs off the page edge.
`report.html` additionally gets `print-report.css` layered on top, which opens each
of the ten numbered sections on its own page—the convention for a report this
length, as opposed to the five-page `SUMMARY.html`, which reads as one continuous
flow. Run `build_report.py` first if the notebook has changed, then `build_pdf.py`,
both from the repo root.

A [GitHub Actions workflow](.github/workflows/build-report.yml) runs both scripts on
every push, on a clean Ubuntu runner, and fails if the regenerated `report.html`
doesn't match what's committed—so this pipeline reproducing isn't a claim resting on
any one person's local setup. It builds from the notebook's already-stored cell
outputs rather than re-executing it, since the restricted BSA microdata can't be
present in a public runner; see the note at the top of the workflow file.

## Provenance

This analysis began as a project for MA336 *Artificial Intelligence and Machine Learning with
Applications* at the University of Essex, and was subsequently revised and extended for
standalone release: the survey coding was corrected,
every figure recomputed from source, a second (linear-bottleneck) autoencoder and a battery of
robustness checks added, and the longitudinal claim re-tested with a difference-in-differences.

## Data availability & licence

This repository is published **without the raw survey microdata**. The British Social
Attitudes files are supplied under the **UK Data Service End User Licence**, which does not
permit redistribution. See [`data/README.md`](data/README.md) for the exact study numbers
and how to obtain them (free, registration required).

Every figure and table in this repository is a **derived statistical output**—aggregate
summaries, model results and cluster centroids. No individual-level records are reproduced.

- **Code** is released under the [MIT Licence](LICENSE).
- **The report text and figures** are © Bradley Quinlan, 2026, and may be read and cited but
  not reproduced wholesale without permission.

## Citation

If you refer to this work: *Quinlan, B. (2026) "One Coalition, Two Electorates: Cross-Pressure
in the Reform UK Vote."*

Underlying data: NatCen Social Research, *British Social Attitudes Survey* 2024
(UK Data Service SN 9478) and 2014 (SN 7809); MHCLG *English Indices of Deprivation 2019*;
House of Commons Library *2025 Local Elections Handbook and Dataset*.
