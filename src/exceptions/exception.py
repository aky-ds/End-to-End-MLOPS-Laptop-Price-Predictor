import os
from pathlib import Path
import sys
class CustomException(Exception):
    def __init__(self,error_message,error_message_details:sys):
        self.error_message = error_message
        _,_,exc_tb=error_message_details.exc_info()
        
        self.line_no=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename
    
    
    def __str__(self):
        return f'The error is {self.error_message}, in the file {self.file_name}, in the line {self.line_no}'
        