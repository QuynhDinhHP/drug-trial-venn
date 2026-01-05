🧪 Drug Trial Venn Diagram Analyzer

A Python program that analyzes drug trial results using Venn diagrams and set theory. It computes how many people tested positive for individual drugs and drug combinations, compares impact vs effectiveness, and visualizes the results.

⸻

📌 What This Project Does
	•	Uses inclusion–exclusion logic to compute all Venn diagram regions
	•	Identifies:
	•	Greatest and smallest impact (largest/smallest Venn sector)
	•	Overall (marginal) effectiveness of each drug
	•	Prevents invalid inputs (e.g., positives exceeding group size)
	•	Visuali◊zes results using matplotlib-venn

⚠️ Effectiveness is reported as overall effectiveness (positives ÷ everyone who received the drug, including overlaps).

⸻

▶️ How to Run
◊
Step 1: Create and Activate a Virtual Environment (Recommended)

python3 -m venv .venv
source .venv/bin/activate

On Windows:

.venv\\Scripts\\activate


⸻

Step 2: Install Required Libraries

pip install -r requirements.txt


⸻

Step 3: Run the Program

python main.py


⸻

Step 4: Follow the Prompts

You will be asked to enter:
	•	Total number of people tested (U)
	•	Total positives (A ∪ B ∪ C)
	•	Positives for each drug (A, B, C)
	•	Pairwise overlaps:
	•	A ∩ B
	•	A ∩ C
	•	B ∩ C
	•	Optional group sizes (enter 0 if unknown)

The program validates all inputs and will re-prompt if values are impossible.

⸻

Step 5: View the Output

The program will:
	•	Compute all Venn diagram sectors
	•	Identify:
	•	Greatest impact (largest sector)
	•	Worst impact (smallest sector)
	•	Calculate overall effectiveness when group sizes are provided
	•	Display a labeled Venn diagram

⸻

📊 Interpretation Notes
	•	Impact = number of positive cases in a Venn sector
	•	Overall effectiveness = positives ÷ everyone who received the drug
	•	Effectiveness includes people who took multiple drugs
	•	Isolated (only-one-drug) effectiveness is not assumed unless exact