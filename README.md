# Lab 6: Code and Branch Coverage Analysis

## Project Details
- **Repository:** L6_L7_12_cloud_storage_tier
- **Application:** `cloud_storage_tier.py`
- **Starter Tests:** `test_cloud_storage.py`
- **Language:** Python 3

## Objective
To measure application code coverage and branch coverage, identify untested paths, and improve test completeness using pytest and coverage.py.

## Dependencies
Install the required dependencies:

```bash
pip install coverage pytest
```

## Test Files

| File | Description |
|---|---|
| `cloud_storage_tier.py` | Application module under test |
| `test_cloud_storage.py` | Original starter test file |
| `CodeCoverageTest_12_cloud_storage_tier.py` | Additional tests for code coverage |
| `BranchCoverageTest_12_cloud_storage_tier.py` | Tests targeting decision branches |
| `code_coverage.png` | Terminal screenshot of code coverage results |
| `branch_coverage.png` | Terminal screenshot of branch coverage results |

## Running Code Coverage

Run the code-coverage test file:

```bash
python -m coverage erase
python -m coverage run -m pytest CodeCoverageTest_12_cloud_storage_tier.py
python -m coverage report -m cloud_storage_tier.py
```

The recorded result was **100% code coverage**, with all 9 tests passing.

## Running Branch Coverage

Run the branch-coverage test file:

```bash
python -m coverage erase
python -m coverage run --branch -m pytest BranchCoverageTest_12_cloud_storage_tier.py
python -m coverage report -m cloud_storage_tier.py
```

Branch coverage measures whether the alternative outcomes of decision statements have been exercised. The target for this lab is at least 90% branch coverage.

## Deliverables
1. Code coverage terminal screenshot.
2. Branch coverage terminal screenshot.
3. `CodeCoverageTest_12_cloud_storage_tier.py`
4. `BranchCoverageTest_12_cloud_storage_tier.py`
5. At least two Git commits, one for code coverage and one for branch coverage.

## Git Commits

- `5ddb09e` — Add code coverage tests and screenshot
- `d7db0de` — Add branch coverage tests and screenshot

## Conclusion
Additional automated tests were written for the cloud storage tier application. Code coverage reached 100% in the recorded report. Branch coverage should be verified using the branch-enabled coverage report before submission.
