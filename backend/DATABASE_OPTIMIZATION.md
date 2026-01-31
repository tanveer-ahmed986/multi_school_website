# Database Optimization Guide (T206)

## Query Performance Optimization

### Index Strategy

All critical queries have been optimized with proper indexes. Current indexes:

#### Schools Table
```sql
CREATE INDEX idx_schools_subdomain ON schools(subdomain);
CREATE INDEX idx_schools_is_active ON schools(is_active);
```

#### Users Table
```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_school_id ON users(school_id);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_email_school ON users(email, school_id);  -- Composite for login
```

#### Faculty Table
```sql
CREATE INDEX idx_faculty_school_id ON faculty(school_id);
CREATE INDEX idx_faculty_visible ON faculty(school_id, is_visible);  -- For public API
```

#### Results Table
```sql
CREATE INDEX idx_results_school_id ON results(school_id);
CREATE INDEX idx_results_published ON results(school_id, is_published);
CREATE INDEX idx_results_lookup ON results(school_id, academic_year, class_level);  -- For filtering
```

#### Notices Table
```sql
CREATE INDEX idx_notices_school_id ON notices(school_id);
CREATE INDEX idx_notices_active ON notices(school_id, expiry_date) WHERE expiry_date > NOW();
CREATE INDEX idx_notices_priority ON notices(school_id, priority DESC, published_date DESC);
```

#### Gallery Images Table
```sql
CREATE INDEX idx_gallery_school_id ON gallery_images(school_id);
CREATE INDEX idx_gallery_category ON gallery_images(school_id, category);
```

#### Audit Logs Table
```sql
CREATE INDEX idx_audit_school_id ON audit_logs(school_id);
CREATE INDEX idx_audit_timestamp ON audit_logs(timestamp DESC);
CREATE INDEX idx_audit_user ON audit_logs(user_id, timestamp DESC);
```

#### Refresh Tokens Table
```sql
CREATE INDEX idx_refresh_tokens_user ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_expires ON refresh_tokens(expires_at);
```

### Analyzing Query Performance

Use `EXPLAIN ANALYZE` to check query performance:

```sql
-- Check faculty query performance
EXPLAIN ANALYZE
SELECT * FROM faculty
WHERE school_id = 'school-uuid'
  AND is_visible = true;

-- Check notices query with filters
EXPLAIN ANALYZE
SELECT * FROM notices
WHERE school_id = 'school-uuid'
  AND expiry_date > NOW()
ORDER BY priority DESC, published_date DESC
LIMIT 10;

-- Check results lookup
EXPLAIN ANALYZE
SELECT * FROM results
WHERE school_id = 'school-uuid'
  AND academic_year = '2024-25'
  AND class_level = 'Class 10';
```

### Query Optimization Checklist

- [x] All foreign keys have indexes
- [x] Frequently filtered columns have indexes
- [x] Composite indexes for multi-column WHERE clauses
- [x] Indexes on ORDER BY columns
- [x] Partial indexes for filtered queries (e.g., `WHERE expiry_date > NOW()`)
- [x] Covering indexes for frequently accessed column combinations

### Common Slow Query Patterns to Avoid

#### ❌ Bad: N+1 Query Problem
```python
# Fetches schools, then queries users for each school
schools = db.query(School).all()
for school in schools:
    users = db.query(User).filter(User.school_id == school.id).all()
```

#### ✅ Good: Use JOIN or eager loading
```python
# Single query with JOIN
schools = db.query(School).options(
    joinedload(School.users)
).all()
```

#### ❌ Bad: SELECT * from large tables
```python
# Fetches all columns including JSONB result_data
results = db.query(Result).filter(Result.school_id == school_id).all()
```

#### ✅ Good: Select only needed columns
```python
# Only fetch metadata, not full result_data
results = db.query(
    Result.id,
    Result.academic_year,
    Result.class_level,
    Result.is_published
).filter(Result.school_id == school_id).all()
```

#### ❌ Bad: Full table scan without limits
```python
# Can return millions of audit logs
logs = db.query(AuditLog).all()
```

#### ✅ Good: Pagination with limits
```python
# Paginate with LIMIT and OFFSET
logs = db.query(AuditLog)\
    .order_by(AuditLog.timestamp.desc())\
    .limit(50)\
    .offset(page * 50)\
    .all()
```

### RLS Performance Considerations

Row-Level Security (RLS) policies add overhead. Optimization strategies:

1. **Session context is set once per request** (in tenant middleware)
```sql
SET app.current_school_id = 'school-uuid';
```

2. **RLS policies use indexed columns**
```sql
-- Policy efficiently uses school_id index
CREATE POLICY tenant_isolation ON faculty
    USING (school_id::text = current_setting('app.current_school_id', TRUE));
```

3. **Monitor RLS overhead with EXPLAIN**
```sql
EXPLAIN ANALYZE
SELECT * FROM faculty;  -- With RLS enabled
```

### Monitoring Query Performance

#### PostgreSQL slow query log

Enable in `postgresql.conf`:
```ini
log_min_duration_statement = 1000  # Log queries taking > 1 second
log_statement = 'all'  # Log all statements (development only)
```

#### Common slow queries to watch

1. **Faculty with photos** (JSONB field)
2. **Results with full data** (large JSONB)
3. **Audit logs** (grows infinitely)
4. **Gallery images** (file paths)

### Caching Strategy

Critical queries are cached (see `cache_service.py`):

- **School config**: 1 hour TTL
- **Public faculty**: 10 minutes TTL
- **Published results**: 30 minutes TTL
- **Active notices**: 5 minutes TTL
- **Gallery images**: 10 minutes TTL

Cache is invalidated on:
- Content updates (PUT/POST/DELETE requests)
- School configuration changes
- Manual cache clear

### Performance Targets

- **Simple queries** (id lookup): <5ms
- **Filtered queries** (with indexes): <50ms
- **Complex queries** (joins, aggregations): <200ms
- **Full-text search**: <500ms

### Maintenance Tasks

#### Weekly
```sql
-- Analyze table statistics
ANALYZE faculty;
ANALYZE results;
ANALYZE notices;
```

#### Monthly
```sql
-- Vacuum and analyze all tables
VACUUM ANALYZE;

-- Reindex if needed (rare)
REINDEX TABLE faculty;
```

#### Quarterly
```sql
-- Archive old audit logs (> 1 year)
DELETE FROM audit_logs WHERE timestamp < NOW() - INTERVAL '1 year';
```

## Performance Monitoring

Use `pg_stat_statements` extension:

```sql
CREATE EXTENSION pg_stat_statements;

-- View slowest queries
SELECT
    mean_exec_time,
    calls,
    query
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

## Database Connection Pooling

Use connection pooling (SQLAlchemy default):

```python
# backend/src/database/connection.py
engine = create_engine(
    DATABASE_URL,
    pool_size=10,           # Max connections in pool
    max_overflow=20,        # Additional connections if pool exhausted
    pool_timeout=30,        # Timeout waiting for connection
    pool_recycle=3600,      # Recycle connections after 1 hour
    echo=False              # Disable SQL logging in production
)
```

## Resources

- [PostgreSQL Performance Tips](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [EXPLAIN ANALYZE Tutorial](https://www.postgresql.org/docs/current/using-explain.html)
- [Index Types in PostgreSQL](https://www.postgresql.org/docs/current/indexes-types.html)
