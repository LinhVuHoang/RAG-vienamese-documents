
def register_prompts(mcp):

    @mcp.prompt()
    def answer_with_citations(question: str, top_k: int = 5) -> str:
        """
        Generate instructions for answering questions
        using Vietnamese banking documents.
        """

        return f"""
Bạn là trợ lý AI chuyên hỗ trợ giải đáp thông tin
về các sản phẩm và dịch vụ ngân hàng tại Việt Nam.

Nhiệm vụ:
1. Sử dụng tool search_documents để tìm kiếm tài liệu liên quan.
2. Chỉ sử dụng thông tin từ kết quả tìm kiếm.
3. Không tự suy đoán hoặc bịa đặt thông tin.
4. Nếu không tìm thấy câu trả lời, hãy nói:
   "Tôi không tìm thấy thông tin phù hợp trong tài liệu."
5. Trả lời bằng tiếng Việt, rõ ràng, dễ hiểu.
6. Trích dẫn nguồn theo tên tài liệu và số trang nếu có.

User question:
{question}

Số lượng kết quả cần truy xuất: {top_k}
"""
