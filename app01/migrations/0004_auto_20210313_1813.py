# Generated by Django 3.1.7 on 2021-03-13 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20210313_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertitle',
            name='stateUser',
            field=models.IntegerField(choices=[(0, '0初次爬取'), (1, '1ksVideo'), (2, '1ksLive'), (3, '2ksVideo+ksLive'), (4, '3videoMP4'), (5, '4vieo+liveMP4')], default=0, verbose_name='用户信息状态'),
        ),
        migrations.AlterField(
            model_name='uservideo',
            name='stateVideo',
            field=models.IntegerField(choices=[(1, '默认ksVideo'), (2, 'ksVideo+ksLive')], default=1, verbose_name='状态'),
        ),
        migrations.CreateModel(
            name='UserPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photoID', models.CharField(default='xxxxxxxx', max_length=128, verbose_name='相册id')),
                ('caption', models.CharField(default='暂无', max_length=512, verbose_name='相册描述')),
                ('displayView', models.CharField(default='-1', max_length=32, verbose_name='播放量')),
                ('displayLike', models.CharField(default='-1', max_length=32, verbose_name='点赞数')),
                ('displayComment', models.CharField(default='-1', max_length=32, verbose_name='评论数')),
                ('imgUrls', models.CharField(default=' ', max_length=5000)),
                ('theUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.usertitle')),
            ],
        ),
    ]
