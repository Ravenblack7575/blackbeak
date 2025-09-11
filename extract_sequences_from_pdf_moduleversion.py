import PyPDF2
import re
import json
from pathlib import Path
import pandas as pd

def extract_sequences_from_pdf(pdf_path):
    
    """
    Extract DNA sequences from PDF
    
    Args:
        pdf_path (Path): Path to the PDF file

    Returns:
        json: List of extracted primer and probe sequences
        csv: List of extracted primer and probe sequences 
        
    """

    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    
    sequences = []
    
    # Pattern 1: "Name: ATCGATCG" or "Name ATCGATCG"
    matches1 = re.findall(r'([A-Za-z0-9_-]+)[\s:]+([ATCGUNRYKMSWBDHVI]{15,40})', text, re.IGNORECASE)
    for name, seq in matches1:
        sequences.append({"name": name, "sequence": seq.upper(), "source": pdf_path.name})
    
    # Pattenr 1b: "Name: 5'-ATCGATCG-3'"
    matches1b = re.findall(r'([A-Za-z0-9_-]+)[\s:]+5\'-([ATCGUNRYKMSWBDHVI]{15,40})-3\'', text, re.IGNORECASE)
    for name, seq in matches1b:
        sequences.append({"name": name, "sequence": seq.upper(), "source": pdf_path.name})
    
    # Pattern 2: "Forward primer: ATCGATCG"
    matches2 = re.findall(r'(Forward|Reverse)\s+primer[\s:]+([ATCGUNRYKMSWBDHVI]{15,40})', text, re.IGNORECASE)
    for name, seq in matches2:
        sequences.append({"name": f"{name}_primer", "sequence": seq.upper(), "source": pdf_path.name})
    
    # Pattern 3: Table format with tabs/spaces
    matches3 = re.findall(r'([A-Za-z0-9_-]+)\s{3,}([ATCGUNRYKMSWBDHVI]{15,40})', text, re.IGNORECASE)
    for name, seq in matches3:
        sequences.append({"name": name, "sequence": seq.upper(), "source": pdf_path.name})
    
    # Pattern 4: Named probes "ProbeName: FAM-ATCGATCG-BHQ1"
    matches4a = re.findall(r'([A-Za-z0-9_-]+)[\s:]+([A-Za-z0-9]+)-([ATCGUNRYKMSWBDHVI]{15,40})-([A-Za-z0-9]+)', text, re.IGNORECASE)
    for name, dye, seq, quencher in matches4a:
        sequences.append({"name": name, "sequence": seq.upper(), "source": pdf_path.name, "dye": dye, "quencher": quencher})
    
    # # Pattern 4b: Unnamed probes "FAM-ATCGATCG-BHQ1" (fallback)
    # matches4b = re.findall(r'([A-Za-z0-9]+)-([ATCGUNRYKMSWBDHVI]{15,40})-([A-Za-z0-9]+)', text, re.IGNORECASE)
    # for dye, seq, quencher in matches4b:
    #     sequences.append({"name": f"{dye}_{quencher}_probe", "sequence": seq.upper(), "source": pdf_path.name})
    
    # Pattern 5a: Named probes "ProbeName: [FAM]ATCGATCG[BHQ1]"
    matches5a = re.findall(r'([A-Za-z0-9_-]+)[\s:]+\[([A-Za-z0-9-]+)\]([ATCGUNRYKMSWBDHVI]{15,40})\[([A-Za-z0-9-]+)\]', text, re.IGNORECASE)
    for name, dye, seq, quencher in matches5a:
        sequences.append({"name": name, "sequence": seq.upper(), "source": pdf_path.name, "dye": dye, "quencher": quencher})
    
    # # Pattern 5b: Unnamed probes "[FAM]ATCGATCG[BHQ1]" (fallback)
    # matches5b = re.findall(r'\[([A-Za-z0-9-]+)\]([ATCGUNRYKMSWBDHVI]{15,40})\[([A-Za-z0-9-]+)\]', text, re.IGNORECASE)
    # for dye, seq, quencher in matches5b:
    #     sequences.append({"name": f"{dye}_{quencher}_probe", "sequence": seq.upper(), "source": pdf_path.name})

    # Pattern 5c: Named probes "ProbeName: (FAM) ATCGATCG (BHQ1)"
    matches5c = re.findall(r'([A-Za-z0-9_-]+)[\s:]+\(([A-Za-z0-9-]+)\)\s*([ATCGUNRYKMSWBDHVI]{15,40})\s*\(([A-Za-z0-9-]+)\)', text, re.IGNORECASE)
    for name, dye, seq, quencher in matches5c:
        sequences.append({"name": name, "sequence": seq.upper(), "source": pdf_path.name, "dye": dye, "quencher": quencher})  
    
    return sequences

def main():
    all_sequences = []
    
    for pdf_file in Path("./papers").glob("*.pdf"):
        print(f"Processing {pdf_file.name}...")
        sequences = extract_sequences_from_pdf(pdf_file)
        all_sequences.extend(sequences)
    
    # Save results
    with open("sequences.json", 'w') as f:
        json.dump(all_sequences, f, indent=2)
    
    # Convert to CSV
    df = pd.DataFrame(all_sequences)
    df.to_csv("sequences.csv", index=False)
    
    print(f"Found {len(all_sequences)} sequences")
    print("Saved to sequences.json and sequences.csv")

if __name__ == "__main__":
    main()