from pydantic import BaseModel, Field
from typing import List

class RequirementItem(BaseModel):
    requirement_number: int = Field(..., description="رقم المتطلب التسلسلي من 1 إلى 22", ge=1, le=22)
    document_page_number: int = Field(..., description="رقم الصفحة في المستند التي يوجد بها هذا المتطلب")
    axis_number: int = Field(..., description="رقم المحور التابع له المتطلب من 1 إلى 5", ge=1, le=5)
    axis_name: str = Field(..., description="اسم المحور باللغة العربية")
    question: str = Field(..., description="نص السؤال التدقيقي الذي يبدأ بـ هل")
    requirement_definition: str = Field(..., description="الشرح التفصيلي لتعريف المتطلب")
    evidence_examples: List[str] = Field(..., description="قائمة تحتوي على أمثلة الشواهد المطلوبة لإثبات الاستيفاء")
    evidence_format: str = Field(..., description="الصيغة الفنية لملف الشاهد مثل PDF, URL, Excel")
    counts_toward_inclusivity_index: bool = Field(..., description="هل يدخل المتطلب ضمن مؤشر الشمولية الرقمية أم لا")

class RequirementsEnvelope(BaseModel):
    requirements: List[RequirementItem] = Field(..., description="مصفوفة تحتوي على كافة المتطلبات الـ 22 المستخرجة")