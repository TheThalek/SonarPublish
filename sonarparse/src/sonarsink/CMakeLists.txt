set(SRC
    sonarsink.c
    )

set(HDR
    )

set(PUBLIC_HDR
    sonarsink.h)

target_sources(${TARGET_LIB}
    PRIVATE ${SRC} ${HDR}
    PUBLIC ${PUBLIC_HDR}
)