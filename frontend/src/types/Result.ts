/**
 * Result entity type definition
 */
export interface ResultSummary {
  result_id: string;
  academic_year: string;
  class_level: string;
  exam_type: string;
  published_date: string;
}

export interface StudentResult {
  roll_number: string;
  student_name: string;
  total_marks: number;
  percentage: number;
  grade: string;
  rank?: number;
  subjects: SubjectResult[];
}

export interface SubjectResult {
  subject_name: string;
  marks_obtained: number;
  max_marks: number;
  grade: string;
}

export interface ResultStatistics {
  total_students: number;
  pass_percentage: number;
  highest_marks: number;
  average_percentage: number;
}

export interface ResultData {
  students: StudentResult[];
  statistics: ResultStatistics;
}

export interface Result extends ResultSummary {
  result_data: ResultData;
}
