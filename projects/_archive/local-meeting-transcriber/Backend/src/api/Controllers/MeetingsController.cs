using Backend.DTOs;
using Backend.Models;
using Backend.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace Backend.Controllers;
[ApiController]
[Route("api/meetings")]
[Authorize]
public class MeetingsController : ControllerBase
{
    private readonly AppDbContext _db;
    private readonly IWebHostEnvironment _env;
    private readonly IConfiguration _cfg;
    private readonly TranscriptionService _transcriber;
    private readonly SummaryService _summarizer;
    private readonly ILogger<MeetingsController> _logger;

    public MeetingsController(AppDbContext db, IWebHostEnvironment env, IConfiguration cfg,
        TranscriptionService t, SummaryService s, ILogger<MeetingsController> logger)
    { 
        _db = db; 
        _env = env; 
        _cfg = cfg; 
        _transcriber = t; 
        _summarizer = s; 
        _logger = logger;
    }

    [HttpPost("upload")]
    [RequestSizeLimit(200_000_000)]
    public async Task<ActionResult<MeetingResponse>> Upload([FromForm] IFormFile file, [FromForm] string? title)
    {
        var userId = User.Claims.First(c => c.Type == "sub").Value;
        _logger.LogInformation("📤 UPLOAD request received from user: {UserId}, file: {FileName}, title: {Title}", 
            userId, file?.FileName, title);
        
        try
        {
            var uploadsRoot = Path.Combine(_env.ContentRootPath, _cfg["Storage:UploadsPath"] ?? "uploads");
            Directory.CreateDirectory(uploadsRoot);

            var fileName = $"{Guid.NewGuid()}_{file.FileName}";
            var fullPath = Path.Combine(uploadsRoot, fileName);
            
            _logger.LogInformation("💾 Saving file to: {FilePath}", fullPath);
            using (var fs = System.IO.File.Create(fullPath))
                await file.CopyToAsync(fs);

            var meeting = new Meeting { UserId = userId, Title = title, AudioPath = fullPath };
            _db.Meetings.Add(meeting);
            await _db.SaveChangesAsync();
            
            _logger.LogInformation("✅ Meeting created with ID: {MeetingId}", meeting.Id);

            // Async post-process (simple inline for MVP)
            _logger.LogInformation("🎵 Starting audio processing for meeting: {MeetingId}", meeting.Id);
            
            var normalized = await FfmpegAudio.ToWav16kMonoAsync(fullPath, Path.GetDirectoryName(fullPath)!);
            _logger.LogInformation("🎵 Audio normalized, starting transcription...");
            
            var (trans, diar) = await _transcriber.TranscribeAsync(normalized);
            _logger.LogInformation("📝 Transcription completed, starting summary...");
            
            var summary = await _summarizer.SummarizeAsync(diar ?? trans);
            _logger.LogInformation("📋 Summary completed for meeting: {MeetingId}", meeting.Id);
            
            meeting.Transcript = trans;
            meeting.DiarizedTranscript = diar;
            meeting.Summary = summary;
            await _db.SaveChangesAsync();

            _logger.LogInformation("✅ UPLOAD completed successfully for meeting: {MeetingId}", meeting.Id);
            return ToDto(meeting);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "💥 UPLOAD error for user: {UserId}", userId);
            throw;
        }
    }

    [HttpGet]
    public async Task<IEnumerable<MeetingResponse>> List()
    {
        var userId = User.Claims.First(c => c.Type == "sub").Value;
        _logger.LogInformation("📋 LIST request received from user: {UserId}", userId);
        
        try
        {
            var items = await _db.Meetings.Where(m => m.UserId == userId)
                .OrderByDescending(m => m.CreatedUtc).ToListAsync();
            
            _logger.LogInformation("📋 Found {Count} meetings for user: {UserId}", items.Count, userId);
            return items.Select(ToDto);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "💥 LIST error for user: {UserId}", userId);
            throw;
        }
    }

    [HttpGet("{id:int}")]
    public async Task<ActionResult<MeetingResponse>> Get(int id)
    {
        var userId = User.Claims.First(c => c.Type == "sub").Value;
        _logger.LogInformation("🔍 GET request for meeting: {MeetingId} from user: {UserId}", id, userId);
        
        try
        {
            var m = await _db.Meetings.FirstOrDefaultAsync(x => x.Id == id && x.UserId == userId);
            if (m is null)
            {
                _logger.LogWarning("❌ Meeting not found: {MeetingId} for user: {UserId}", id, userId);
                return NotFound();
            }
            
            _logger.LogInformation("✅ Meeting found: {MeetingId} for user: {UserId}", id, userId);
            return ToDto(m);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "💥 GET error for meeting: {MeetingId}, user: {UserId}", id, userId);
            throw;
        }
    }

    private MeetingResponse ToDto(Meeting m) =>
        new(m.Id, m.Title, $"/file/{Path.GetFileName(m.AudioPath)}", m.Summary, m.Transcript, m.DiarizedTranscript, m.CreatedUtc.ToString("o"));
}
