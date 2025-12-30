from django import forms

from .models import Project


def _split_lines(value):
    if not value:
        return []
    lines = [line.strip() for line in value.splitlines() if line.strip()]
    if len(lines) == 1 and "," in lines[0]:
        lines = [item.strip() for item in lines[0].split(",") if item.strip()]
    return lines


def _parse_usage_items(value):
    items = []
    for line in _split_lines(value):
        parts = [part.strip() for part in line.split("|")]
        if len(parts) == 1:
            parts = [part.strip() for part in line.split(",")]
        if len(parts) == 1:
            parts = [part.strip() for part in line.split(":")]
        if not parts or not parts[0]:
            continue
        label = parts[0]
        percent = None
        note = ""
        if len(parts) > 1 and parts[1]:
            try:
                percent = float(parts[1])
            except ValueError:
                percent = None
        if len(parts) > 2 and parts[2]:
            note = parts[2]
        if percent is None:
            continue
        items.append({"label": label, "percent": percent, "note": note})
    return items


class ProjectForm(forms.ModelForm):
    tech_stack_text = forms.CharField(
        label="기술 스택",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        help_text="줄바꿈 또는 쉼표로 항목을 입력하세요.",
    )
    details_text = forms.CharField(
        label="상세 설명",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        help_text="줄바꿈으로 항목을 구분합니다.",
    )
    highlights_text = forms.CharField(
        label="5줄 요약",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        help_text="줄바꿈으로 항목을 구분합니다.",
    )
    usage_items_text = forms.CharField(
        label="사용 비중 항목",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        help_text="한 줄에 '이름 | 퍼센트 | 메모' 형식으로 입력하세요.",
    )

    class Meta:
        model = Project
        fields = [
            "name",
            "summary",
            "link",
            "usage_title",
            "usage_type",
            "note",
            "order",
        ]
        labels = {
            "name": "프로젝트 이름",
            "summary": "요약",
            "link": "링크",
            "usage_title": "그래프 제목",
            "usage_type": "그래프 유형",
            "note": "참고 문구",
            "order": "정렬 순서",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "summary": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "link": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://"}),
            "usage_title": forms.TextInput(attrs={"class": "form-control"}),
            "usage_type": forms.Select(attrs={"class": "form-select"}),
            "note": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "order": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["usage_type"].choices = [
            ("", "선택 안 함"),
            (Project.USAGE_LANGUAGE, "언어"),
            (Project.USAGE_TOOL, "도구"),
            (Project.USAGE_OTHER, "기타"),
        ]
        self.fields["order"].required = False
        self.fields["order"].help_text = "비워두면 자동으로 마지막 순서에 추가됩니다."

        if self.instance.pk:
            self.fields["tech_stack_text"].initial = "\n".join(self.instance.tech_stack or [])
            self.fields["details_text"].initial = "\n".join(self.instance.details or [])
            self.fields["highlights_text"].initial = "\n".join(self.instance.highlights or [])
            usage_lines = []
            for item in self.instance.usage_items or []:
                label = item.get("label", "")
                percent = item.get("percent", "")
                note = item.get("note", "")
                if note:
                    usage_lines.append(f"{label} | {percent} | {note}")
                else:
                    usage_lines.append(f"{label} | {percent}")
            self.fields["usage_items_text"].initial = "\n".join(usage_lines)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.tech_stack = _split_lines(self.cleaned_data.get("tech_stack_text", ""))
        instance.details = _split_lines(self.cleaned_data.get("details_text", ""))
        instance.highlights = _split_lines(self.cleaned_data.get("highlights_text", ""))
        instance.usage_items = _parse_usage_items(self.cleaned_data.get("usage_items_text", ""))
        if instance.order is None:
            instance.order = 0
        if commit:
            instance.save()
        return instance
