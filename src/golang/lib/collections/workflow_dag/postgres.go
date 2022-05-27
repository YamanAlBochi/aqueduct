package workflow_dag

type postgresReaderImpl struct {
	standardReaderImpl
}

type postgresWriterImpl struct {
	standardWriterImpl
}

func newPostgresReader() Reader {
	return &postgresReaderImpl{standardReaderImpl{}}
}

func newPostgresWriter() Writer {
	return &postgresWriterImpl{standardWriterImpl{}}
}
