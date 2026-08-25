# TempleOSRS and Wise Old Man API Patterns

## TempleOSRS (templeosrs.com/api/v2)
- Base URL: `https://templeosrs.com/api/v2`
- No API key required for basic endpoints
- Common endpoints:
  - `/player/{username}/info` - Player profile
  - `/player/{username}/stats` - All skill levels/XP
  - `/player/{username}/gains?period=d|w|m` - XP gains
  - `/groups/{groupid}/memberstats` - Clan member stats
  - `/skill-hiscores?skill={skill}` - Skill-specific hiscores

## Wise Old Man (api.wiseoldman.net/v2)
- Base URL: `https://api.wiseoldman.net/v2`
- Basic endpoints require no key
- Higher rate limits with WOM_API_KEY
- Common endpoints:
  - `/player/{username}/info` - Player profile
  - `/player/{username}/stats` - Skill levels
  - `/player/{username}/gains` - Recent XP gains
  - `/player/{username}/achievements` - Achievement data
  - `/groups/{groupid}/memberstats` - Group member stats

## HTTP Client Usage
```java
// Using Java 11+ HttpClient
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://templeosrs.com/api/v2/player/" + username + "/stats"))
    .GET()
    .build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
String json = response.body();
```

## Error Handling
- Check response status codes
- Handle malformed JSON gracefully
- Implement caching for rate limit avoidance
- Network timeouts: 5 seconds max
