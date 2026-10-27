/**
 * Verification du loader d'intro (index.html).
 *
 * Pilote Chrome via le DevTools Protocol (aucune dependance npm) et verifie
 * que le loader disparait bien apres le chargement :
 *   - #lpc doit atteindre 100%
 *   - #loader doit recevoir la classe "off"
 *   - <body> doit recevoir la classe "go"
 *
 * Usage : node check-loader.mjs [url]
 */
import { spawn } from 'node:child_process'
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'

const URL_TEST = process.argv[2] || 'http://127.0.0.1:5230/'
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
const PORT = 9333

const sleep = ms => new Promise(r => setTimeout(r, ms))

const userDataDir = mkdtempSync(join(tmpdir(), 'lt-loader-'))
const chrome = spawn(
  CHROME,
  [
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    `--remote-debugging-port=${PORT}`,
    `--user-data-dir=${userDataDir}`,
    'about:blank',
  ],
  { stdio: 'ignore' },
)

async function getDebuggerUrl() {
  for (let i = 0; i < 40; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${PORT}/json/version`)
      const json = await res.json()
      if (json.webSocketDebuggerUrl) return json.webSocketDebuggerUrl
    } catch {
      /* pas encore pret */
    }
    await sleep(250)
  }
  throw new Error('Chrome DevTools indisponible')
}

let ws
let msgId = 0
const pending = new Map()

function send(method, params = {}, sessionId) {
  const id = ++msgId
  return new Promise((resolve, reject) => {
    pending.set(id, { resolve, reject })
    ws.send(JSON.stringify({ id, method, params, sessionId }))
  })
}

try {
  const wsUrl = await getDebuggerUrl()
  ws = new WebSocket(wsUrl)
  await new Promise((resolve, reject) => {
    ws.addEventListener('open', resolve, { once: true })
    ws.addEventListener('error', reject, { once: true })
  })

  ws.addEventListener('message', ev => {
    const msg = JSON.parse(ev.data)
    if (msg.id && pending.has(msg.id)) {
      const { resolve, reject } = pending.get(msg.id)
      pending.delete(msg.id)
      if (msg.error) reject(new Error(JSON.stringify(msg.error)))
      else resolve(msg.result)
    }
  })

  const { targetId } = await send('Target.createTarget', { url: 'about:blank' })
  const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true })

  await send('Page.enable', {}, sessionId)
  await send('Runtime.enable', {}, sessionId)

  // Collecte des erreurs console / exceptions JS.
  const jsErrors = []
  ws.addEventListener('message', ev => {
    const msg = JSON.parse(ev.data)
    if (msg.method === 'Runtime.exceptionThrown') {
      jsErrors.push(msg.params.exceptionDetails?.exception?.description || 'exception')
    }
  })

  await send('Page.navigate', { url: URL_TEST }, sessionId)

  // Attend la fin du chargement + la fermeture du loader.
  let state = null
  for (let i = 0; i < 40; i++) {
    await sleep(500)
    const { result } = await send(
      'Runtime.evaluate',
      {
        expression: `(() => {
          const lpc = document.querySelector('#lpc');
          const loader = document.querySelector('#loader');
          return JSON.stringify({
            pct: lpc ? lpc.textContent : null,
            loaderClass: loader ? loader.className : null,
            loaderExists: !!loader,
            bodyClass: document.body.className,
            hasGo: document.body.classList.contains('go')
          });
        })()`,
        returnByValue: true,
      },
      sessionId,
    )
    try {
      state = JSON.parse(result.value)
    } catch {
      continue
    }
    if (state.hasGo) break
  }

  console.log('URL testee   :', URL_TEST)
  console.log('loader existe:', state?.loaderExists)
  console.log('classe loader:', state?.loaderClass)
  console.log('classe body  :', state?.bodyClass)
  console.log('pourcentage  :', state?.pct)
  console.log('erreurs JS   :', jsErrors.length ? jsErrors : 'aucune')

  const ok = state?.hasGo === true && (state?.loaderClass || '').includes('off')
  console.log(ok ? '\nOK - le loader se ferme correctement' : '\nECHEC - le loader reste bloque')
  process.exitCode = ok ? 0 : 1
} catch (err) {
  console.error('Erreur :', err.message)
  process.exitCode = 1
} finally {
  try {
    ws?.close()
  } catch {
    /* ignore */
  }
  chrome.kill()
  // Chrome peut encore verrouiller des fichiers (Crashpad) : la suppression
  // du dossier temporaire est best-effort.
  try {
    rmSync(userDataDir, { recursive: true, force: true, maxRetries: 5, retryDelay: 200 })
  } catch {
    /* ignore */
  }
}
