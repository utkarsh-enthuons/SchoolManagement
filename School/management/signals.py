from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Students, FeePayment

@receiver(post_save, sender=Students)
def create_fee_payment(sender, instance, created, **kwargs):
    if created:
        # Assuming the student has an attribute 'admission_class_id' or related field
        # that points to the class the student is associated with.
        student_class = instance.admission_class  # Replace this with the actual attribute for class if different

        if student_class:
            FeePayment.objects.create(
                student_id=instance,
                class_id=student_class,
                phone_number=instance.phone_number,
                monthly_fee=0,
                admission_fee=0,
                first_quarter_exam_fee=0,
                half_year_exam_fee=0,
                second_quarter_exam_fee=0,
                annual_exam_fee=0,
                board_reg_fee=0,
                board_fee=0,
                admit_card_fee=0,
                practical_1_fee=0,
                practical_2_fee=0,
                practical_3_fee=0,
                practical_4_fee=0,
            )
