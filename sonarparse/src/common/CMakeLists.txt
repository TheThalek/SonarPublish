set(SRC
    sonarmeta.c
	sonarshared.c
    )

set(HDR
    )

set(PUBLIC_HDR
    sonarmeta.h
	sonarshared.h
    )

target_sources(${TARGET_LIB}
    PRIVATE ${SRC} ${HDR}
    PUBLIC ${PUBLIC_HDR}
)