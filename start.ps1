Write-Host "Starting CrimeSense AI..." -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/2] Starting Backend..." -ForegroundColor Yellow
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-m uvicorn main:app --host 0.0.0.0 --port 8000 --reload" -WorkingDirectory "backend"
Start-Sleep -Seconds 3

Write-Host "[2/2] Starting Frontend..." -ForegroundColor Yellow
Start-Process -NoNewWindow -FilePath "npx" -ArgumentList "next dev --turbopack" -WorkingDirectory "frontend"

Write-Host ""
Write-Host "CrimeSense AI is starting up!" -ForegroundColor Green
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
