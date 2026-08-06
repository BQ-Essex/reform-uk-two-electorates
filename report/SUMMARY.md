# One Coalition, Two Electorates

### A short, code-free tour of what the data showed about Reform UK's voters

*Bradley Quinlan, 2026*

*This is the plain-language version of the project. The full write-up, with all the code, is in
the [notebook](../notebook/) and rendered for reading in [`report.html`](report.html). Every chart
here is a statistic computed from survey data—no individual respondents are shown.*

---

## The question

There's a comfortable shorthand in political commentary: "the Reform voter." I wanted to know
whether that single label hides more than one kind of person.

The starting idea is **cross-pressure**—a classic in electoral sociology. A voter can hold
attitudes that pull against their own vote. Ford and Goodwin (2014) describe this kind of base as
"left behind": socially hardline, but economically dependent on the state—a claim others have since contested (Evans and Mellon, 2016) or reframed around identity and education (Sobolewska and Ford, 2020, in *Brexitland*). Rather than assert
the tension exists, I wanted to test whether it actually shows up *inside* Reform's 2024 voters—using machine learning, and using several methods so they could check each other.

## Where the data made me change course

Three honest moments shaped the result, and I've left them visible rather than tidied away.

**A plan the data wouldn't support.** I'd intended to study LGB Reform voters and their own
equality attitudes. But the survey's split-ballot design meant that of 336 Reform voters, only
fifteen identified as non-heterosexual, and just two of those were asked the relevant questions.
Two is not a finding. So I reframed the question from *identity-versus-vote* to
*attitude-versus-attitude*—the stronger question anyway.

**A judgement call over a metric.** After using PCA to find the main attitudinal axes, I clustered
the voters. The usual metric (the silhouette score) was highest at two clusters—but two clusters
lumped almost all Reform voters together and hid exactly what I was looking for. I chose three,
transparently trading a little statistical neatness for a result that answered the question. (As it
happens, the two-cluster optimum *is* the two-electorates story; the third cluster is just a small
left-libertarian fringe.)

**A method that disagreed with itself.** A first autoencoder seemed to confirm the clusters
neatly—until I noticed its result leaned on a geometric quirk. A second one, built to remove the
quirk, disagreed. Instead of quietly keeping the flattering number, I followed the disagreement,
and it led to the most useful part of the analysis: pinning down exactly how much to trust the split.

## The finding: two electorates, not one

Clustered on political attitudes alone, Reform's voters split almost in half:

- **55%** sit in a conventional **right-authoritarian** group.
- **41%** sit in an **authoritarian-left** group—socially hardline, but economically left:
  strongly pro-redistribution and left-leaning, and with a majority receiving benefits.

That second group is the cross-pressured one. Their economic instincts sit in real tension with the
party they voted for—Reform campaigned in 2024 on tax cuts it costed itself at nearly £90bn a year, a figure
the IFS reported and judged an underestimate (Emmerson, Joyce and Miller, 2024). But "economically left"
undersells what's actually going on. This group is pro-redistribution *and* about as sceptical of
welfare claimants as the conventional right-authoritarian group *and* nearly as anti-immigration
(around four in five, on the relevant split-ballot items, rate immigration bad for the economy). It's
their *benefit reliance*, not sympathy for claimants, that makes the "left-behind" label concrete.
Redistribution to an implied in-group, alongside hostility to an out-group's claim on the same welfare
state, is what political scientists call **welfare chauvinism** (Andersen and Bjørklund, 1990)—a more
precise description than "a left-wing electorate inside a right-wing party."

![The two attitudinal axes: PC1 (left–right fusion) and PC2 (authoritarian-left vs libertarian-right)](../figures/fig03_pca-biplot.png)

![The three-cluster solution: ~55% right-authoritarian, ~41% authoritarian-left](../figures/fig05_kmeans-clusters-k3-scatter.png)

## Is it real—and is it old?

**How much to trust it.** The autoencoder that disagreed taught me where the uncertainty really
lives. The split barely moves if I drop the weakest variable, cluster on the full data instead of a
2-D summary, or resample the respondents—a Reform voter placed in the left-behind group stays there
across resamples 98% of the time. Hierarchical clustering agrees with the main method strongly, and a
decision tree, coming at the problem backwards, finds the same dominant attitude and—tellingly—struggles to pick out the cross-pressured group, exactly as a genuinely conflicted group should. The
one thing that *can* redraw the split is a radically different way of compressing the data, and even
then only at the soft border between the two Reform groups, never in whether the left-behind group
exists.

**How old it is.** Projecting 2014 UKIP identifiers into the same model, they fall into the
"left-behind" cluster *even more heavily* than 2024 Reform voters—59% against 41%, a gap well beyond
chance. The pattern predates Reform by a decade. Looking closer, Reform's coalition hasn't *moved away*
from the left-behind core so much as *added* a conventional-right layer on top of it: the left-behind
group is still over-represented, while the conventional-right group flips from under- to
over-represented over the ten years.

## What I'm claiming—and what I'm not

I've kept the claims honest. This is **descriptive**, the subgroups are small, and the clustering is unweighted—though reweighting the Reform split to the survey's published weights barely changes it (52/44/4 against 55/41/4), so the two-electorates finding isn't an artefact of that. These are not turnout predictions, and a repeated snapshot a decade apart can show the profile is durable without proving how individuals moved. But across linear and non-linear methods,
supervised and unsupervised, and across ten years of data, the same structure keeps surfacing: a single
"Reform voter" label hides two quite different electorates, and the cross-pressured half is real,
robust, and at least a decade old.

---

## Works cited

Andersen, J.G. and Bjørklund, T. (1990) 'Structural Changes and New Cleavages: the Progress Parties
in Denmark and Norway', *Acta Sociologica*, 33(3), pp. 195–217.

Emmerson, C., Joyce, R. and Miller, H. (2024) *Reform UK manifesto: a reaction*. London: Institute
for Fiscal Studies. Available at: <https://ifs.org.uk/articles/reform-uk-manifesto-reaction>
(Accessed: 6 August 2026).

Evans, G. and Mellon, J. (2016) 'Working Class Votes and Conservative Losses: Solving the UKIP
Puzzle', *Parliamentary Affairs*, 69(2), pp. 464–479.

Ford, R. and Goodwin, M.J. (2014) *Revolt on the Right: Explaining Support for the Radical Right in
Britain*. Abingdon: Routledge.

Sobolewska, M. and Ford, R. (2020) *Brexitland: Identity, Diversity and the Reshaping of British
Politics*. Cambridge: Cambridge University Press.

The full reference list is in [`report.html`](report.html).

---

*Data: British Social Attitudes Survey 2024 (UK Data Service SN 9478) and 2014 (SN 7809), NatCen
Social Research; English Indices of Deprivation 2019 (MHCLG); 2025 Local Elections Handbook (House
of Commons Library). The raw survey microdata is licence-restricted and not included in this
repository—see [`data/README.md`](../data/README.md).*
