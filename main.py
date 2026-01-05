from matplotlib_venn import venn3
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def ask_group_size(name, positives, total_tested):
    """Ask user for group size until a valid number is given (0 = unknown)."""
    while True:
        try:
            n = int(input(f"Enter total tested in group {name} (0 if unknown): "))

            if n == 0:
                return 0

            if n < positives:
                print(f"❌ Invalid: {name} must be at least {positives} (positives). Try again.")
                continue

            if n > total_tested:
                print(f"❌ Invalid: {name} cannot exceed total tested U={total_tested}. Try again.")
                continue

            return n
        except ValueError:
            print("⚠️ Please enter an integer.")


def ask_for_values():
    print("=== Drug Trial Venn Diagram Calculator (Interactive Mode) ===")
    total_tested = int(input("Enter total number of people tested (U): "))
    AuBuC = int(input("Enter total positives in A ∪ B ∪ C (union): "))

    # Totals (positives by drug, including overlaps)
    A_total = int(input("Enter positives in Drug A (A): "))
    B_total = int(input("Enter positives in Drug B (B): "))
    C_total = int(input("Enter positives in Drug C (C): "))

    # Pairwise overlaps (positives)
    AB = int(input("Enter positives in A ∩ B (AB): "))
    AC = int(input("Enter positives in A ∩ C (AC): "))
    BC = int(input("Enter positives in B ∩ C (BC): "))

    # Optional denominators for overall effectiveness (0 = unknown)
    nA = ask_group_size("A", A_total, total_tested)
    nB = ask_group_size("B", B_total, total_tested)
    nC = ask_group_size("C", C_total, total_tested)

    return total_tested, AuBuC, A_total, B_total, C_total, AB, AC, BC, nA, nB, nC


def drug_trial_analysis(total_tested, AuBuC, A_total, B_total, C_total, AB, AC, BC, nA, nB, nC):
    """
    IMPORTANT:
    A_total, B_total, C_total are total positives for each drug (including overlaps).
    AB, AC, BC are total positives in intersections (including triple overlap).
    """

    # --- inclusion-exclusion for triple overlap ---
    ABC = -(A_total + B_total + C_total) + (AB + AC + BC) + AuBuC

    # sector-only overlaps
    onlyAB = AB - ABC
    onlyAC = AC - ABC
    onlyBC = BC - ABC

    # only-one-drug sectors
    onlyA = A_total - (onlyAB + onlyAC + ABC)
    onlyB = B_total - (onlyAB + onlyBC + ABC)
    onlyC = C_total - (onlyAC + onlyBC + ABC)

    none = total_tested - AuBuC

    # --- basic sanity check so diagram doesn't go weird ---
    sectors_all = [onlyA, onlyB, onlyC, onlyAB, onlyAC, onlyBC, ABC, none]
    if any(x < 0 for x in sectors_all):
        print("\n❌ Inputs are inconsistent (some sectors became negative).")
        print("Check that AB ≤ min(A,B), AC ≤ min(A,C), BC ≤ min(B,C), and union is correct.")
        return

    if (onlyA + onlyB + onlyC + onlyAB + onlyAC + onlyBC + ABC) != AuBuC:
        print("\n❌ Inputs are inconsistent (sector positives do not add up to union).")
        return

    # --- print sector counts (impact) ---
    print("\n=== Sector counts (Impact by exact regimen) ===")
    print(f"only A: {onlyA}")
    print(f"only B: {onlyB}")
    print(f"only C: {onlyC}")
    print(f"A∩B only: {onlyAB}")
    print(f"A∩C only: {onlyAC}")
    print(f"B∩C only: {onlyBC}")
    print(f"A∩B∩C: {ABC}")
    print(f"None (negative for all): {none}")

    sectors = {
        "only A": onlyA,
        "only B": onlyB,
        "only C": onlyC,
        "A∩B only": onlyAB,
        "A∩C only": onlyAC,
        "B∩C only": onlyBC,
        "A∩B∩C": ABC
    }

    best_sector = max(sectors, key=sectors.get)
    worst_sector = min(sectors, key=sectors.get)
    print(f"\n👉 Greatest impact sector: {best_sector} = {sectors[best_sector]}")
    print(f"👉 Worst impact sector: {worst_sector} = {sectors[worst_sector]}")

    # --- overall (marginal) effectiveness: positives / everyone who received the drug ---
    print("\n=== Overall positive response rate (NOT isolated) ===")
    print("Reminder: This includes people who may have received multiple drugs.\n")

    if nA > 0:
        print(f"Drug A overall rate = {A_total}/{nA} = {A_total/nA:.1%}")
    else:
        print("Drug A overall rate = Unknown (nA not provided)")

    if nB > 0:
        print(f"Drug B overall rate = {B_total}/{nB} = {B_total/nB:.1%}")
    else:
        print("Drug B overall rate = Unknown (nB not provided)")

    if nC > 0:
        print(f"Drug C overall rate = {C_total}/{nC} = {C_total/nC:.1%}")
    else:
        print("Drug C overall rate = Unknown (nC not provided)")

    print("\n" + "-" * 55 + "\n")  # spacing before diagram

    # --- Draw Venn diagram ---
    fig, ax = plt.subplots(figsize=(7, 7))
    v = venn3(
        subsets=(onlyA, onlyB, onlyAB, onlyC, onlyAC, onlyBC, ABC),
        set_labels=("Drug A", "Drug B", "Drug C"),
        ax=ax
    )

    for region_id in ['100', '010', '001', '110', '101', '011', '111']:
        patch = v.get_patch_by_id(region_id)
        if patch:
            patch.set_edgecolor("black")
            patch.set_linewidth(2)

    plt.title("Drug Testing", fontsize=14)

    # universe grey box (your tuned coordinates)
    rect = patches.Rectangle(
        (-1.28, -0.95), 2.56, 2.55,
        linewidth=2, edgecolor='black', facecolor='lightgrey',
        zorder=-1
    )
    ax.add_patch(rect)
    ax.set_xlim(-1.28, 1.28)
    ax.set_ylim(-0.95, 1.40)

    ax.text(0.05, 1.05, f"U = {total_tested}",
            fontsize=12, fontweight='bold', ha='left', va='top',
            transform=ax.transAxes)

    # show "none" count in the outside region
    ax.text(0.55, -0.6, f"{none}", fontsize=10)

    plt.axis("off")
    plt.show()


def run_example():
    # Your example dataset (already consistent)
    total_tested = 50
    union = 41
    A_total = 21
    B_total = 21
    C_total = 31
    AB = 9
    AC = 14
    BC = 15
    nA, nB, nC = 0, 0, 0  # unknown denominators
    drug_trial_analysis(total_tested, union, A_total, B_total, C_total, AB, AC, BC, nA, nB, nC)


def main():
    print("Choose mode:")
    print("1) Run built-in example")
    print("2) Interactive input")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        run_example()
    else:
        args = ask_for_values()
        drug_trial_analysis(*args)


if __name__ == "__main__":
    main()