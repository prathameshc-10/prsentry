from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class PullRequest(Base):
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True)
    repo_name = Column(String, nullable=False)
    pr_number = Column(Integer, nullable=False)
    status = Column(String, default="open")
    created_at = Column(DateTime, default=datetime.utcnow)

    review_runs = relationship("ReviewRun", back_populates="pull_request")


class ReviewRun(Base):
    __tablename__ = "review_runs"

    id = Column(Integer, primary_key=True)
    pr_id = Column(Integer, ForeignKey("pull_requests.id"), nullable=False)
    status = Column(String, default="pending")  # pending -> running -> completed / failed
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    pull_request = relationship("PullRequest", back_populates="review_runs")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    review_run_id = Column(Integer, ForeignKey("review_runs.id"), nullable=False)
    agent_name = Column(String, nullable=False)  # style, security, test_coverage
    finding_type = Column(String, nullable=True)
    severity = Column(String, nullable=True)
    message = Column(Text, nullable=False)
    file_path = Column(String, nullable=True)
    line_number = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)