# Generated by Django 4.2.3 on 2023-07-04 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS_Core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authors',
            options={'verbose_name': 'Authors', 'verbose_name_plural': 'Authors'},
        ),
        migrations.AlterModelOptions(
            name='books',
            options={'verbose_name': 'Books', 'verbose_name_plural': 'Books'},
        ),
        migrations.AlterField(
            model_name='authors',
            name='books',
            field=models.ManyToManyField(blank=True, to='LMS_Core.books', verbose_name='Books of the Author'),
        ),
        migrations.CreateModel(
            name='BookLending',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrower', models.JSONField(verbose_name='Borrower Information')),
                ('borrow_date', models.DateField(verbose_name='Borrow Date')),
                ('due_date', models.DateField(verbose_name='Due Date')),
                ('book_returned', models.BooleanField(blank=True, default=False)),
                ('return_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('book', models.ManyToManyField(to='LMS_Core.books', verbose_name='Borrowed Books')),
            ],
            options={
                'verbose_name': 'Book Lending History',
                'verbose_name_plural': 'Book Lending History',
            },
        ),
    ]
