"""
Celery tasks for paragraph processing.

This module contains asynchronous tasks that are executed by Celery workers
for background processing of paragraph data.
"""

from celery import shared_task


@shared_task
def process_paragraph(text):
    """
    Asynchronously process a paragraph and calculate word frequency.
    
    This task is triggered when a new paragraph is created. It analyzes
    the text and counts the frequency of each word in lowercase.
    
    Args:
        text (str): The paragraph text to process
    
    Returns:
        dict: Dictionary with words as keys and their frequency counts as values
        
    Example:
        >>> process_paragraph("hello world hello python")
        {'hello': 2, 'world': 1, 'python': 1}
    
    Notes:
        - Text is converted to lowercase before processing
        - Words are separated by whitespace
        - Results are printed to console/logs
        - This is an async task, so it doesn't block the HTTP response
    """

    words = text.lower().split()

    frequency = {}

    for word in words:

        if word in frequency:

            frequency[word] += 1

        else:

            frequency[word] = 1

    print("Word Frequency:", frequency)

    return frequency