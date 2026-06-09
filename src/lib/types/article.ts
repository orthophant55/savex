export type ArticleCategory =
  | "game_review"
  | "player_analysis"
  | "team_analysis"
  | "sabermetrics";

export type ArticleSourceType = "ai_generated" | "editorial" | "hybrid";

export type AiGenerationStatus =
  | "pending"
  | "generating"
  | "completed"
  | "failed"
  | "review_needed";

export interface ArticleRelated {
  gameId?: string;
  playerIds?: string[];
  teamIds?: string[];
}

export interface Article {
  id: string;
  title: string;
  summary: string;
  body: string; // markdown or plain text
  category: ArticleCategory;
  sourceType: ArticleSourceType;
  aiGenerationStatus?: AiGenerationStatus;
  publishedAt: string; // ISO 8601
  updatedAt?: string;
  author?: string; // AI 생성의 경우 "KBO Insight AI"
  related: ArticleRelated;
  tags: string[];
  thumbnailColor?: string; // placeholder 색상
  readingTimeMinutes: number;
}
