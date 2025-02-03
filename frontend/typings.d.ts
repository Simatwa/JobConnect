export type Jobs = {
    id: number;
    title: string;
    type: string;
    category_id: number;
    category_name: string;
    company_id: number;
    company_username: string;
    min_salary: number;
    max_salary: number;
    updated_at: string;
    location: string;
  };

  type JobCategory = "all" | "full-time" | "internship";
