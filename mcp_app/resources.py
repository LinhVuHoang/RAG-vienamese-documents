import json
from src.config.config import RAW_DIR

def register_resources(mcp):
    
    @mcp.resource("banking://documents")
    
    def list_document() -> str:
        
        """
        List all PDF documents available in the RAG storage
        """
        
        RAW_DIR.mkdir(parents=True,exist_ok=True)
        
        documents =[]
        
        for pdf_file in sorted(RAW_DIR.glob("*.pdf")):
            
            documents.append({
                
                "File_name": pdf_file.name.split(pdf_file.name.split("_")[0])[1].strip("_"),
                "Size": pdf_file.stat().st_size,
                "Format":"PDF"
            })
            
        result = {
            "Documents": documents,
            "Total": len(documents)
        }
        
        return json.dumps(
            result,
            ensure_ascii=False,
            indent=2
        )
            
