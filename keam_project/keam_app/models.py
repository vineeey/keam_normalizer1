from django.db import models
from django.db.models import Avg


class Year(models.Model):
    value = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return str(self.value)

    def get_global_stats(self):
        """Get global mean and SD for all subjects for this year"""
        subjects = SubjectStat.objects.filter(board__year=self).values_list('subject', flat=True).distinct()
        stats = {}

        for subject in subjects:
            subject_stats = SubjectStat.objects.filter(
                board__year=self,
                subject__iexact=subject
            ).aggregate(
                global_mean=Avg('mean'),
                global_sd=Avg('sd')
            )
            stats[subject.lower()] = {
                'mean': subject_stats['global_mean'] or 70.0,
                'sd': subject_stats['global_sd'] or 10.0
            }

        # Ensure we have stats for all required subjects
        required_subjects = ['mathematics', 'physics', 'chemistry']
        for subject in required_subjects:
            if subject not in stats:
                stats[subject] = {'mean': 70.0, 'sd': 10.0}

        return stats

    class Meta:
        ordering = ['-value']
        verbose_name = "Academic Year"
        verbose_name_plural = "Academic Years"


class Board(models.Model):
    name = models.CharField(max_length=100)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    max_mark = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"{self.name} ({self.year})"

    class Meta:
        ordering = ['year', 'name']
        unique_together = ('name', 'year')


class SubjectStat(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    mean = models.FloatField()
    sd = models.FloatField()
    max_mark = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"{self.board.name} - {self.subject}"

    class Meta:
        ordering = ['board__year', 'board__name', 'subject']
        verbose_name = "Subject Statistics"
        verbose_name_plural = "Subject Statistics"