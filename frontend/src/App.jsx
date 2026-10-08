import { useState } from 'react'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [report, setReport] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  function handleFileChange(event) {
    setFile(event.target.files[0] ?? null)
    setReport(null)
    setError('')
  }

  async function handleAnalyze(event) {
    event.preventDefault()
    if (!file || loading) return

    setLoading(true)
    setReport(null)
    setError('')

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          typeof data.detail === 'string'
            ? data.detail
            : 'Could not analyze this file.',
        )
      }

      setReport(data)
    } catch (error) {
      setError(
        error instanceof TypeError || error instanceof SyntaxError
          ? 'Could not reach the analysis service. Check that both servers are running.'
          : error.message,
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="workbench">
      <h1>CSV Quality Workbench</h1>
      <p>Check your CSV for blank values and duplicate rows.</p>

      <form onSubmit={handleAnalyze}>
        <label htmlFor="csv-file">Choose a CSV file</label>
        <input
          id="csv-file"
          type="file"
          accept=".csv,text/csv"
          onChange={handleFileChange}
          disabled={loading}
        />
        <p>UTF-8 encoding · Maximum 5 MiB</p>

        <button type="submit" disabled={!file || loading}>
          {loading ? 'Analyzing…' : 'Analyze'}
        </button>
      </form>

      {loading && <p role="status">Analyzing your file…</p>}
      {error && <p role="alert">{error}</p>}

      {report && (
        <section aria-labelledby="report-heading">
          <h2 id="report-heading">Analysis report</h2>

          <dl>
            <dt>Rows</dt>
            <dd>{report.row_count}</dd>
            <dt>Columns</dt>
            <dd>{report.column_count}</dd>
            <dt>Duplicate rows</dt>
            <dd>{report.duplicate_count}</dd>
          </dl>

          <h3>Blank values by column</h3>
          <table>
            <thead>
              <tr>
                <th scope="col">Column</th>
                <th scope="col">Blank values</th>
              </tr>
            </thead>
            <tbody>
              {report.columns.map((column) => (
                <tr key={column}>
                  <th scope="row">{column}</th>
                  <td>{report.blank_counts[column]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}
    </main>
  )
}

export default App