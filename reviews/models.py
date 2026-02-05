from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    # 主键由Django自动创建（id字段），无需手动定义
    rating = models.PositiveSmallIntegerField(
        '评分',
        validators=[
            MinValueValidator(1, message="评分不能低于1分"),
            MaxValueValidator(5, message="评分不能高于5分")
        ],
        help_text="请输入1-5分的整数评分"
    )

    content = models.TextField(
        '评价内容',
        max_length=1000,
        blank=False,  # 强制要求填写内容
        help_text="请输入评价内容（最多1000字）"
    )

    created_at = models.DateTimeField(
        '评价时间',
        auto_now_add=True  # 自动记录创建时间
    )

    # 外键关联（假设评价者模型为 Evaluator，键盘模型为 Keyboard）
    evaluator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # 评价者删除则关联评价同步删除
        verbose_name='评价者',
        related_name='reviews'
    )

    keyboard = models.ForeignKey(
        'keyboards.Keyboard',
        on_delete=models.CASCADE,  # 键盘删除则关联评价同步删除
        verbose_name='关联键盘',
        related_name='reviews'
    )

    class Meta:
        verbose_name = '用户评价'
        verbose_name_plural = '用户评价列表'
        ordering = ['-created_at']  # 默认按最新评价排序
        unique_together = ['evaluator', 'keyboard']  # 同一用户对同一键盘只能评价一次

    def __str__(self):
        return f"{self.evaluator.username} 对 {self.keyboard.name} 的 {self.rating} 星评价"

    # 自定义验证（可选）
    def clean(self):
        from django.core.exceptions import ValidationError

        # 验证内容长度
        if len(self.content.strip()) < 10:
            raise ValidationError({'content': '评价内容至少需要10个有效字符'})