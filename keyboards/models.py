from django.db import models
from django.core.validators import MinValueValidator


class Keyboard(models.Model):
    # 字段定义
    name = models.CharField(
        '键盘名称',
        max_length=100,
        unique=True,  # 保证名称唯一性
        help_text="请输入键盘型号名称（如：Keychron Q3）"
    )

    switch_type = models.CharField(
        '轴体类型',
        max_length=50,
        help_text="请输入轴体类型（如：Cherry MX红轴）"
    )

    layout = models.CharField(
        '配列',
        max_length=20,
        help_text="键盘布局（如：100%、80%、TKL）"
    )

    CONNECTION_CHOICES = [
        ('wired', '有线'),
        ('bluetooth', '蓝牙'),
        ('2.4g', '2.4G无线'),
        ('Dual-mode', '有线/无线双模'),
        ('Three-mode', '有线/无线/蓝牙三模'),
    ]
    connection = models.CharField(
        '连接方式',
        max_length=20,
        choices=CONNECTION_CHOICES,
        default='wired'
    )

    battery_capacity = models.PositiveIntegerField(
        '电池容量(mAh)',
        null=True,
        blank=True,  # 允许为空（有线键盘无需电池）
        help_text="无线键盘需填写电池容量"
    )

    price = models.DecimalField(
        '价格',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]  # 价格必须大于0
    )

    release_date = models.DateField(
        '上市日期',
        auto_now=False,  # 禁用自动填充
        auto_now_add=False,  # 禁用自动填充
    help_text = "请输入上市日期（格式：YYYY-MM-DD）"
    )

    # 元数据
    class Meta:
        verbose_name = '键盘信息'  # 单数显示名称
        verbose_name_plural = '键盘信息'  # 复数显示名称
        ordering = ['-release_date']  # 默认按上市日期倒序排列

    def __str__(self):
        return f"{self.name} ({self.switch_type})"

    # 自定义验证（可选）
    def clean(self):
        from django.core.exceptions import ValidationError

        # 验证无线键盘必须填写电池容量
        if self.connection != 'wired' and not self.battery_capacity:
            raise ValidationError({'battery_capacity': '无线连接方式必须填写电池容量'})