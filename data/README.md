# Data

## Included in this repository (open licences, redistributable with attribution)

| File | Source | Licence |
|------|--------|---------|
| `IoD2019_LA_upper_tier.xlsx` | English Indices of Deprivation 2019—Ministry of Housing, Communities & Local Government | Open Government Licence v3.0 |
| `LEH-2025-results-HoC.xlsx` | 2025 Local Elections Handbook and Dataset—House of Commons Library (Rallings, Thrasher & Bunting, Elections Centre, University of Exeter) | Open Parliament Licence |

## NOT included (restricted—you must obtain these yourself)

The British Social Attitudes microdata is supplied under the **UK Data Service End User
Licence**, which prohibits redistribution. It is free to download after registering for a
UK Data Service account.

| Needed file | Dataset | UK Data Service study | DOI |
|-------------|---------|----------------------|-----|
| `p19056-bsa24-archive.tab` | British Social Attitudes Survey, 2024 (NatCen) | **SN 9478** | 10.5255/UKDA-SN-9478-1 |
| `bsa14_final.tab` | British Social Attitudes Survey, 2014 (NatCen) | **SN 7809** | 10.5255/UKDA-SN-7809-2 |

### How to obtain them

1. Register for a free account at <https://ukdataservice.ac.uk/>.
2. Search for the study numbers above (SN 9478 and SN 7809).
3. Download the **tab-delimited** version and accept the End User Licence.
4. Place the two `.tab` files in this `data/` folder using the exact filenames in the table.

Once both files are present, the notebook runs end to end.

### Two things to expect when you do

**Filenames.** The notebook reads the two paths exactly as spelled in the table above.
`bsa14_final.tab` is simply the SN 7809 tab-delimited file renamed—it is the full released
dataset (2,878 respondents × 726 variables), not a locally prepared extract. Either rename
your download to match, or adjust the `read_csv` lines in the notebook.

**Variable naming differs between the two years, and the notebook relies on that.** The 2014
file spells the attitude scales in lower case (`libauth`, `leftrigh`, `welfare2`, `redistrb`)
where 2024 uses initial capitals (`Libauth`, `Welfare2`, `Redistrb`). `TaxSpend` is
capitalised in both. In 2014, `libauth`, `leftrigh` and `welfare2` also arrive as *strings*
rather than numerics, with `' '` for "no self-completion" and `'9'` for missing—Section 10
coerces them explicitly. These are properties of the released files, not of this project.
