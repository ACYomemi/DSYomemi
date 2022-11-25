# Generated by Django 4.1.2 on 2022-11-03 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Compulsory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept', models.CharField(max_length=2)),
                ('course', models.CharField(max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='CourseInfo',
            fields=[
                ('courseID', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('score', models.DecimalField(decimal_places=0, max_digits=2)),
                ('descript', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('studentID', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
                ('pwd', models.DecimalField(decimal_places=0, max_digits=6)),
                ('dept', models.CharField(max_length=2)),
                ('totalScore', models.DecimalField(decimal_places=0, default=0, max_digits=3)),
                ('compulsoryScore', models.DecimalField(decimal_places=0, default=0, max_digits=3)),
                ('totalGPA', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('compulsoryGPA', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherInfo',
            fields=[
                ('teacherID', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
                ('pwd', models.DecimalField(decimal_places=0, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('teacherID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studentID_Notice', to='Yomemi.teacherinfo')),
            ],
        ),
        migrations.CreateModel(
            name='CourseSelect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('courseID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courseID_CourseSelect', to='Yomemi.courseinfo')),
                ('studentID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studentID_CourseSelect', to='Yomemi.studentinfo')),
            ],
        ),
        migrations.AddField(
            model_name='courseinfo',
            name='teacherID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacherID_CourseInfo', to='Yomemi.teacherinfo'),
        ),
        migrations.AddConstraint(
            model_name='courseinfo',
            constraint=models.CheckConstraint(check=models.Q(('score__gte', 0), ('score__lte', 10)), name='CourseInfoScore'),
        ),
    ]