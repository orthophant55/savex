"""Article topic ranking model — mock placeholder.

Replace rank_topics() with a trained classifier or LLM-based topic extractor.
"""

from app.ml.contracts import ArticleTopicInput, ArticleTopicOutput


class ArticleTopicModel:
    model_name = "article_topic_v0"
    model_version = "0.1.0-mock"

    def rank_topics(self, input: ArticleTopicInput) -> ArticleTopicOutput:
        topics = []
        category = "sabermetric_column"

        if input.game_id:
            topics.append("경기 결과 분석")
            topics.append("승리 기여도 (WPA)")
            category = "game_recap"

        if input.player_ids:
            topics.append("선수 성적 분석")
            topics.append("세이버매트릭스 지표 해석")
            category = "player_analysis"

        if input.team_ids and not input.player_ids:
            topics.append("팀 전력 분석")
            topics.append("시즌 전망")
            category = "team_analysis"

        if not topics:
            topics = ["리그 동향", "통계 분석"]

        return ArticleTopicOutput(
            ranked_topics=topics,
            suggested_category=category,
            confidence=0.55,
        )
