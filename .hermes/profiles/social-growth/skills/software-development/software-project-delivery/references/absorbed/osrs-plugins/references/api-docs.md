# OSRS Plugin API Documentation

## WiseOldMan API

### Endpoints
- `GET /player/{name}/gains` - Returns 7-day XP gains
- `GET /player/{name}/stats` - Returns player stats including total XP

### Response Format
```json
{
  "total_gained": 123456,
  "xp": 987654321,
  "date": "2024-01-01T00:00:00Z"
}
```

### Authentication
- No API key required for public endpoints
- Respect rate limits (500 requests/hour per IP)

### Example Request
```bash
curl "https://secure.runescape.com/m=ws/player/LocalPlayerName/gains"
```

## TempleOSRS API

### Endpoints
- `GET /player/{name}/gains` - Returns 7-day XP gains
- `GET /player/{name}/kc` - Returns boss kill counts

### Response Format
```json
{
  "total_gained": 123456,
  "xp": 987654321,
  "date": "2024-01-01T00:00:00Z"
}
```

### Authentication
- No API key required for public endpoints
- Respect rate limits (120 requests/minute per IP)

### Example Request
```bash
curl "https://secure.runescape.com/m=ws/player/LocalPlayerName/gains"
```

## Common Patterns

1. **XP Extraction**: Use regex pattern `(?:total_gained|xp)\\s*[:=]\\s*(\\d+)` to extract XP values from JSON responses
2. **API Fallback**: Use WiseOldMan as primary source, TempleOSRS as secondary fallback
3. **Caching**: Cache API responses for 24 hours to reduce API calls
4. **Error Handling**: Implement retry logic with exponential backoff for transient failures

## Example Code Snippet
```java
public double get7DayXP(String playerName) throws Exception {
    try {
        // Try WiseOldMan first
        String womResponse = WOMApiClient.getPlayerGains(playerName);
        double womXP = parseXPFromResponse(womResponse);
        
        // Try TempleOSRS as fallback
        String templeResponse = TempleApiClient.getPlayerGains(playerName);
        double templeXP = parseXPFromResponse(templeResponse);
        
        return (womXP + templeXP) / 2.0;
    } catch (Exception e) {
        log.warn("Failed to get XP for {}: {}", playerName, e.getMessage());
        return 0;
    }
}