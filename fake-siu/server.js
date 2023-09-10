const jsonServer = require('json-server')

const server = jsonServer.create()
const router = jsonServer.router('db.json')
const middlewares = jsonServer.defaults()

server.use(middlewares)
server.use(jsonServer.rewriter({
  "/docentes/:docente_id/finales/:final_id/subir_acta": "/docentes/:docente_id/actas",
  "/docentes/:docente_id/finales/:final_id/cargar_notas": "/noop",
}))
server.use(jsonServer.bodyParser)
server.use('/noop', (req, res, next) => {
  res.status(200).jsonp({})
})

// Use default router
server.use(router)
server.listen(process.env.PORT || 3000, () => {
  console.log('JSON Server is running')
})