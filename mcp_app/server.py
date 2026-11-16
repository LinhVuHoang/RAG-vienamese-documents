from mcp.server.fastmcp import FastMCP
from src.Pipeline.Indexing_pipeline import IndexingPipeline
from tools import register_tools
from resources import register_resources
from prompts import register_prompts


# Initialize MCP Server
mcp = FastMCP("Vietnamese Document RAG")


# Initialize shared pipeline
indexing_pipeline = IndexingPipeline()


# Register MCP primitives
register_tools(mcp, indexing_pipeline)
register_resources(mcp)
register_prompts(mcp)


# Run MCP Server
if __name__ == "__main__":
    mcp.run(transport="stdio")
